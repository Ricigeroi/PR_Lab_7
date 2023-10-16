import requests
from bs4 import BeautifulSoup


# Function to extract information from a list of URLs
def extract_info(list_of_urls):
    result = []
    for item in list_of_urls:
        result.append(extract_info_from_page(item))
    return result


# Function to extract specific details from a single webpage
def extract_info_from_page(url):
    base_path = "https://999.md"

    # Send a GET request to the URL
    response = requests.get(url)
    # Check for successful response
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None

    # Parse the webpage content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    info = {}

    # Define titles/sections to extract data from
    titles = [
        'Caracteristici',
        'Condiții de utilizare',
        'Adăugător',
        'Subcategorie',
        'Preț',
        'Regiunea',
        'Contacte'
    ]

    # Extract data for each title/section
    for groupTitle in titles:
        section = soup.find('h2', string=groupTitle)

        # Check if the section exists or if it's one of the hardcoded sections
        if section or groupTitle in ['Preț', 'Regiunea', 'Contacte']:
            info[groupTitle] = {}

            # Extract characteristics
            if groupTitle == 'Caracteristici':
                for li in section.find_next('ul').find_all('li', class_='m-value'):
                    key = li.find('span', class_='adPage__content__features__key').text.strip()
                    value = li.find('span', class_='adPage__content__features__value').text.strip()
                    info[groupTitle][key] = value

            # Extract usage conditions
            elif groupTitle == 'Condiții de utilizare':
                for li in section.find_next('ul').find_all('li', class_='m-value'):
                    key = li.find('span', class_='adPage__content__features__key with-rules').text.strip()
                    value = li.find('span', class_='adPage__content__features__key with-rules').text.strip()
                    info[groupTitle][key] = value

            # Extract other data
            elif groupTitle == 'Adăugător':
                for li in section.find_next('ul').find_all('li', class_='m-no_value'):
                    key = li.find('span', class_='adPage__content__features__key').text.strip()
                    info[groupTitle][key] = None

            # Extract subcategory link
            elif groupTitle == 'Subcategorie':
                value = (base_path + soup.find("a", class_="adPage__content__features__category__link").get('href'))
                info[groupTitle] = value

            # Extract price info
            elif groupTitle == 'Preț':
                for ul in soup.find_all('ul', {'class': 'adPage__content__price-feature__prices'}):
                    for li in ul.find_all('li'):
                        if not (
                                not (li.get('class') != ['tooltip', 'adPage__content__price-feature__prices__price',
                                                         'is-main'])
                                or
                                not (li.get('class') != ['tooltip', 'adPage__content__price-feature__prices__price'])
                        ):
                            continue

                        value = li.find('span',
                                        class_='adPage__content__price-feature__prices__price__value').text.strip()
                        currency = li.find('span',
                                           class_='adPage__content__price-feature__prices__price__currency').text.strip()
                        value += ' ' + currency

                        # Map currency symbol to its name
                        currency_names = {
                            '€': 'Euro',
                            'lei': 'Lei',
                            '$': 'USD'
                        }
                        info[groupTitle][currency_names.get(currency, '')] = value

            # Extract region/address
            elif groupTitle == 'Regiunea':
                address = ''
                values = soup.findAll('dd', {'itemprop': 'address'})
                for v in values:
                    address += v.text.strip()
                info[groupTitle] = address

            # Extract contact information
            elif groupTitle == 'Contacte':
                values = soup.findAll('dt', string=groupTitle + ': ')
                if not values:
                    info[groupTitle] = None
                else:
                    for v in values:
                        try:
                            info[groupTitle] = v.find_next('dd').find_next('ul').find_next('li').find('a').get('href')
                        except Exception as e:
                            pass

    return info
