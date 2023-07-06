import requests
from bs4 import BeautifulSoup

def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    # Extract product details
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    for result in results:
        product = {}

        # Product URL
        product['URL'] = 'https://www.amazon.in' + result.find('a', {'class': 'a-link-normal s-no-outline'}).get('href')

        # Product Name
        product['Name'] = result.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()

        # Product Price
        price = result.find('span', {'class': 'a-price-whole'})
        if price:
            product['Price'] = price.text.strip()
        else:
            product['Price'] = 'Not available'

        # Rating
        rating = result.find('span', {'class': 'a-icon-alt'})
        if rating:
            product['Rating'] = rating.text.strip()
        else:
            product['Rating'] = 'Not available'

        # Number of Reviews
        reviews = result.find('span', {'class': 'a-size-base'})
        if reviews:
            product['Reviews'] = reviews.text.strip()
        else:
            product['Reviews'] = 'Not available'

        products.append(product)

    return products

# Scrape 20 pages of product listings
base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
all_products = []

for page in range(1, 21):
    page_url = base_url + str(page)
    products = scrape_product_details(page_url)
    all_products.extend(products)

# Print the scraped product details
for product in all_products:
    print('URL:', product['URL'])
    print('Name:', product['Name'])
    print('Price:', product['Price'])
    print('Rating:', product['Rating'])
    print('Reviews:', product['Reviews'])
    print('---')
