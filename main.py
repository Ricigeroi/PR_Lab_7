import requests
from bs4 import BeautifulSoup


def parse(link, max_page_num=None):
    base_path = "https://999.md"
    result = []
    current_url = link
    flag = True
    try:
        while flag:

            # Send a GET request to the URL
            response = requests.get(current_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:

                # Parse the HTML content of the page
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find paginator and its elements
                paginator_obj = soup.find('nav', class_='paginator cf')
                current_page = paginator_obj.find('li', class_='current')
                paginator_elements = paginator_obj.find_all('li')
                paginator_links = paginator_obj.find_all('a')

                # Limit the number of paged parsed by the function
                if max_page_num and int(current_page.text) > max_page_num:
                    break

                print(f"Processing page {current_page.text}")

                # Find all anchor (link) tags in the HTML
                links = soup.find_all(lambda tag: tag.name == 'a' and tag.get('class') in [['js-item-ad'], ['js-delivery-ad']])

                # Extract and print the href attribute of each link
                for link in links:
                    if link == paginator_links[-1]:
                        break
                    href = link.get('href')

                    # Ignoring boosters and already added links
                    if href and ("/booster" not in href) and (base_path + href not in result):
                        result.append(base_path + href)

                # Break if this page is the last one
                if paginator_elements[-1] == current_page:
                    break
                # Finding URL of the next page
                else:
                    current_url = base_path + paginator_elements[paginator_elements.index(current_page) + 1].find('a').get('href')

            else:
                print(f"Failed to retrieve the web page #{current_page}. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return result


url = "https://999.md/ru/list/transport/spare-parts-for-motorcycles"

result = parse(url, 5)

print(result)
