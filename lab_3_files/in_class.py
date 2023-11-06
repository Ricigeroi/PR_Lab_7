import requests
from bs4 import BeautifulSoup


def parse(link, max_page_num=None, current_page_num=1, result=None):
    if result is None:
        result = []

    base_path = "https://999.md"
    try:
        response = requests.get(link)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')
            paginator_obj = soup.find('nav', class_='paginator cf')
            current_page = paginator_obj.find('li', class_='current')

            # If the current page number exceeds the maximum page number, return the result
            if max_page_num and int(current_page.text) > max_page_num:
                return result

            print(f"Processing page {current_page.text}")

            links = soup.find_all(
                lambda tag: tag.name == 'a' and tag.get('class') in [['js-item-ad'], ['js-delivery-ad']])
            for link in links:
                href = link.get('href')
                if href and ("/booster" not in href) and (base_path + href not in result):
                    result.append(base_path + href)

            # If this is the last page, return the result.
            # Otherwise, call the function recursively with the next page URL.
            next_page = paginator_obj.find('li', class_='current').find_next('li')
            if next_page and next_page.find('a'):
                next_page_url = base_path + next_page.find('a').get('href')

                # RECURSIVE CALL BELOW
                # |
                # |
                # v
                return parse(next_page_url, max_page_num, current_page_num + 1, result)
                # ^
                # |
                # |
                # RECURSIVE CALL ABOVE

            else:
                return result

        else:
            print(f"Failed to retrieve the web page #{current_page}. Status code: {response.status_code}")
            return result

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return result

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return result
