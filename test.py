import requests
from bs4 import BeautifulSoup

def get_profile_data(profile_url):
    response = requests.get(profile_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        portfolios = soup.find_all('h2', class_='css-13merx8')
        portfolio = 'No'

        for item in portfolios:
            if 'Portfolio from the Business' in item.text:
                portfolio = 'Yes'
                break

        get_price = 'Yes' if soup.find('button', class_='css-1ru1z96') else 'No'

        reviews_container = soup.find_all('div', class_='css-1qn0b6x')
        reviews = [{'text': review.find('p', class_='comment__09f24__D0cxf css-qgunke').get_text(), 'date': review.find('span', class_='css-chan6m').get_text()} for review in reviews_container if review.find('p', class_='comment__09f24__D0cxf css-qgunke') and review.find('span', class_='css-chan6m')]
        
        if reviews:
            last_3_reviews = reviews[-3:]
        else:
            last_3_reviews = []
        
        return get_price, portfolio, last_3_reviews
        
    else:
        return None, None, None

def get_yelp_businesses(api_key, location, category, limit):
    # Reemplazar espacios con %20 en la ubicación
    location = location.replace(' ', '%20')

    url = f'https://api.yelp.com/v3/businesses/search?location={location}&term={category}&categories={category}&sort_by=best_match&limit={limit}'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    businesses_data = []

    if response.status_code == 200:
        businesses = response.json()['businesses']
        for business in businesses:
            business_info = {
                "ID": business['id'],
                "Name": business['name'],
                "Alias": business['alias'],
                "Image URL": business['image_url'],
                "URL": business['url'],
                "Review Count": business['review_count'],
                "Rating": business['rating'],
                "Phone": business['phone'],
                "Display Phone": business['display_phone'],
                "Distance": business['distance'],
                "Transactions": business['transactions'],
                "Display Address": business['location']['display_address']
            }

            # Obtener información adicional del perfil
            get_price, portfolio, last_3_reviews = get_profile_data(business_info["URL"])
            business_info["Profile Info"] = {
                "Get Price": get_price,
                "Portfolio": portfolio,
                "Last 3 Reviews": last_3_reviews
            }

            businesses_data.append(business_info)

    else:
        print(f"Error: {response.status_code}")

    return businesses_data


api_key = 'K1wxqUgzSkaPZML_34DUhvfawKSiQ75gKOiIqmL2W2bptLSYFNFKcMGZxajbKhs1SS5tq-hD0B9wmq9GkYnzZW36Gxmfwh9nyc4sN1MqDQJA3IDKl-eg2gN-vUmlZXYx'
location = 'los angeles'
category = 'plumbers'
limit = 5

result = get_yelp_businesses(api_key, location, category, limit)

# Imprimir el resultado para verificar
for business in result:
    print(business)
    print("="*50)
