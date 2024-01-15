from bs4 import BeautifulSoup
from flask import Flask, request, render_template
import requests
from geopy.distance import geodesic

app = Flask(__name__)


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


        #web
        web_class = 'arrange__09f24__LDfbs gutter-2__09f24__CCmUo vertical-align-middle__09f24__zU9sE css-1qn0b6x'
        web_element = soup.find_all('div', class_=web_class)

        web_found = False
        web = None

        for element in web_element:
            text_element = element.find('p', class_='css-1p9ibgf')
            if text_element:
                text = text_element.text.strip()
                if not web_found:
                    web = text
                    web_found = True
                    break
        
        return get_price, portfolio, last_3_reviews, web
        
    else:
        return None, None, None, None

def calculate_distance(user_location, business_location, decimals=2):
    user_latitude, user_longitude = user_location
    business_latitude, business_longitude = business_location
    user_coords = (user_latitude, user_longitude)
    business_coords = (business_latitude, business_longitude)
    
    # Calcular la distancia con geodesic
    distance_in_km = geodesic(user_coords, business_coords).kilometers
    
    # Redondear la distancia al número de decimales especificado
    rounded_distance = round(distance_in_km, decimals)
    
    return rounded_distance

def get_yelp_businesses(api_key, location, category, limit, user_location):
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
        user_latitude, user_longitude = user_location
        region_info = response.json()['region']
        latitude, longitude = region_info['center']['latitude'], region_info['center']['longitude']

        for business in response.json()['businesses']:
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
                "Transactions": business['transactions'],
                "Display Address": business['location']['display_address'],
                "Latitude": latitude,
                "Longitude": longitude,
                "Distance": calculate_distance((user_latitude, user_longitude), (latitude, longitude))
            }

            # Obtener información adicional del perfil
            get_price, portfolio, last_3_reviews, web = get_profile_data(business_info["URL"])
            business_info["Profile Info"] = {
                "Get Price": get_price,
                "Portfolio": portfolio,
                "Website" : web,
                "Last 3 Reviews": last_3_reviews
            }

            businesses_data.append(business_info)

    else:
        print(f"Error: {response.status_code}")

    return businesses_data


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_yelp_businesses():
    api_key = 'K1wxqUgzSkaPZML_34DUhvfawKSiQ75gKOiIqmL2W2bptLSYFNFKcMGZxajbKhs1SS5tq-hD0B9wmq9GkYnzZW36Gxmfwh9nyc4sN1MqDQJA3IDKl-eg2gN-vUmlZXYx'

    user_location = request.form.get('user_location', '')
    category = request.form.get('category', '')
    location = request.form.get('location', '')
    limit = int(request.form.get('limit', 5))

    #user_location = (34.0522, -118.2437)
    user_location = (float(request.form.get('user_latitude', 0)), float(request.form.get('user_longitude', 0)))


    result = get_yelp_businesses(api_key, location, category, limit, user_location)

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)