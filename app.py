from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import unquote
from tqdm import tqdm
import os


# Data
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

# Controller
def save_to_excel(data, filename='business_data.xlsx'):

    if os.path.exists(filename):
        os.remove(filename)

    # Crear un DataFrame con las columnas deseadas
    columns = ["Name", "URL", "Rating", "Phone", "Display Phone", "Display Address",
               "Get Price", "Portfolio", "Website", "Review 1", "Review 1 Date",
               "Review 2", "Review 2 Date", "Review 3", "Review 3 Date", "City"]
    df = pd.DataFrame(columns=columns)

    rows_data = []  # Lista para almacenar todas las filas

    for business_info in data:
        row_data = {
            "Name": business_info.get("Name", ""),
            "URL": business_info.get("URL", ""),
            "Rating": business_info.get("Rating", ""),
            "Phone": business_info.get("Phone", ""),
            "Display Phone": business_info.get("Display Phone", ""),
            "Display Address": ", ".join(business_info.get("Display Address", [])),
            "Get Price": business_info.get("Profile Info", {}).get("Get Price", ""),
            "Portfolio": business_info.get("Profile Info", {}).get("Portfolio", ""),
            "Website": business_info.get("Profile Info", {}).get("Website", ""),
            "City": unquote(business_info.get("city", ""))
        }

        # Obtener las últimas 3 revisiones
        last_3_reviews = business_info.get("Profile Info", {}).get("Last 3 Reviews", [])
        for i, review in enumerate(last_3_reviews, start=1):
            row_data[f"Review {i}"] = review.get("text", "")
            row_data[f"Review {i} Date"] = review.get("date", "")

        # Verificar si la fila tiene algún valor nulo o vacío
        if not any(pd.isna(value) or value == "" for value in row_data.values()):
            rows_data.append(row_data)

    # Añadir todas las filas al DataFrame de una vez
    df = pd.concat([df, pd.DataFrame(rows_data)], ignore_index=True)

    # Guardar en Excel
    df.to_excel(filename, index=False)

def get_yelp_businesses(api_key, locations, category, limit):
    all_businesses_data = []

    offset = 0

    for location in tqdm(locations, desc='Processing locations', unit='location'):
        # Reemplazar espacios con %20 en la ubicación
        location = location.replace(' ', '%20')

        url = f'https://api.yelp.com/v3/businesses/search?location={location}&term={category}&categories={category}&sort_by=best_match&limit={limit}&offset={offset}'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers)

        businesses_data = []

        if response.status_code == 200:
            region_info = response.json()['region']
            latitude, longitude = region_info['center']['latitude'], region_info['center']['longitude']

            for business in tqdm(response.json()['businesses'], desc=f'Processing businesses in {location}', unit='business'):
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
                    "city": location  # Agregar la clave 'city' con el valor de la ubicación actual
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

        all_businesses_data.extend(businesses_data)

    return all_businesses_data

def main():
    api_key = 'K1wxqUgzSkaPZML_34DUhvfawKSiQ75gKOiIqmL2W2bptLSYFNFKcMGZxajbKhs1SS5tq-hD0B9wmq9GkYnzZW36Gxmfwh9nyc4sN1MqDQJA3IDKl-eg2gN-vUmlZXYx'

    categories = 'Plumber'
    #locations = ['Los Angeles', 'Miami', 'Dallas', 'Houston', 'Austin', 'Sacramento', 'San Francisco', 'San Diego', 'Tampa', 'Chicago']
    locations = ['Los Angeles']

    limit = 51

    result = get_yelp_businesses(api_key, locations, categories, limit)

    # Guardar en Excel
    save_to_excel(result)

if __name__ == '__main__':
    main()