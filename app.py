import requests
from bs4 import BeautifulSoup

def get_profile_data(profile_url):
    # Hacer una solicitud HTTP a la página del perfil de Yelp
    response = requests.get(profile_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get Logo
        logo_class = soup.find('img', class_='businessLogo__09f24__jydFo businessLogo--v2__09f24__MfF2g')
        logo = 'No'

        if logo_class:
            logo = 'Yes'

        # Get portfolio
        portfolios = soup.find_all('h2', class_='css-13merx8')
        portfolio = 'No'

        for item in portfolios:
            if 'Portfolio from the Business' in item.text:
                portfolio = 'Yes'
                break

        # Get highlights
        highlights_container = soup.find('div', class_='arrange__09f24__LDfbs gutter-2__09f24__CCmUo layout-wrap__09f24__GEBlv layout-6-units__09f24__pP1H0 css-1qn0b6x')
        highlights = []
        if highlights_container:
            spans = highlights_container.find_all('span', class_='mobile-text-medium__09f24__MZ1v6 css-1dtv2dz')
            for span in spans:
                highlight_text = span.get_text()
                highlights.append(highlight_text)

        if not highlights:
            highlights = 'No'

        # Get pricing and availability
        buttons = soup.find_all('button', class_='css-1ru1z96')
        get_price = ''
        if buttons:
            for button in buttons:
                span_inside_button = button.find('span', class_='css-1enow5j')
                if span_inside_button:
                    get_price = 'Yes'
                else:
                    get_price = 'No'
        else:
            get_price = 'No'

        # Extraer la calificación desde el span con la clase 'css-1p9ibgf'
        rate_class = 'css-1p9ibgf'
        rate_element = soup.find('span', class_=rate_class)

        # Extraer las reseñas y fechas
        reviews_container = soup.find_all('div', class_='css-1qn0b6x')
        reviews = []
        for review in reviews_container:
            review_text = review.find('p', class_='comment__09f24__D0cxf css-qgunke')
            review_date = review.find('span', class_='css-chan6m')

            if review_text and review_date:
                review_info = {
                    'text': review_text.get_text(),
                    'date': review_date.get_text()
                }
                reviews.append(review_info)

        # Encontrar la sección que contiene el teléfono y la página web
        web_and_phone_class = 'arrange__09f24__LDfbs gutter-2__09f24__CCmUo vertical-align-middle__09f24__zU9sE css-1qn0b6x'
        web_and_phone_elements = soup.find_all('div', class_=web_and_phone_class)

        web_found = False
        phone_found = False

        phone, web = None, None

        if web_and_phone_elements:
            for element in web_and_phone_elements:
                text_element = element.find('p', class_='css-1p9ibgf')
                if text_element:
                    text = text_element.text.strip()
                    if not web_found:
                        web = text
                        web_found = True
                    elif not phone_found:
                        phone = text
                        phone_found = True
                        break  # Salir del bucle después de encontrar el número

        if rate_element:
            rate_text = rate_element.text.strip()
            # Extraer solo el valor numérico
            rate_value = float(rate_text.split()[0])
            return rate_value, reviews, phone, web, get_price, highlights, portfolio, logo
        else:
            print(f'Calificación no encontrada en la página del perfil: {profile_url}')
            return None, None, None, None, None, None, None, None
    else:
        print(f"No se pudo obtener la página del perfil. Código de estado: {response.status_code}")
        return None, None, None, None, None, None, None, None
    
def get_business(url):
    # Hacer una solicitud HTTP a la página de Yelp
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        negocios = []
        business_container_class = 'container__09f24__FeTO6 hoverable__09f24___UXLO css-azqg3k'

        businesses = soup.find_all('div', class_=business_container_class)

        for business in businesses[:10]:
            # Extraer nombre del negocio
            business_name_element = business.find('a', class_='css-19v1rkv')

            if business_name_element:
                business_name_text = business_name_element.text.strip()
                business_href = business_name_element['href']
                full_url = 'https://www.yelp.com' + business_href

                # Obtener el tiempo de respuesta
                response_time_element = business.find('span', {'class': ['raqResponseTime', 'raqFastResponder']})
                response_time = response_time_element.text.strip() if response_time_element else 'No response time'


                # Obtener la calificación y las reseñas del perfil
                rate, reviews, phone, website, get_price, highlights, portfolio, logo = get_profile_data(full_url)

                # Añadir el negocio a la lista solo si se obtuvo la calificación
                if rate is not None:
                    # Imprimir solo las últimas 3 reseñas
                    last_3_reviews = reviews[-3:]
                    print(f'Name: {business_name_text}')
                    print(f'Get pricing and availability: {get_price}')
                    print(f'Logo: {logo}')
                    print(f'Portfolio: {portfolio}')
                    print(f'Highlights: {highlights}')
                    print(f'Rate: {rate}')
                    print(f'Phone {phone}')
                    print(f'Website: {website}')
                    print(f'Yelp URL: {full_url}')
                    print(f'Response Time: {response_time}')
                    print(f'Last 3 reviews:')
                    for review in last_3_reviews:
                        print(f'  - {review}')
                    print("=" * 50)

                    # Añadir el negocio a la lista
                    negocios.append({
                        'name': business_name_text,
                        'href': full_url,
                        'rate': rate,
                        'logo': logo,
                        'get_price': get_price,  # Añadir get_price
                        'portfolio': portfolio,  # Añadir portfolio
                        'highlights': highlights,  # Añadir highlights
                        'phone': phone,
                        'website': website,
                        'response_time': response_time,
                        'reviews': last_3_reviews
                    })
        return negocios
    else:
        print(f"No se pudo obtener la página. Código de estado: {response.status_code}")
        return None

# URL de búsqueda en Yelp
url = 'https://www.yelp.com/search?find_desc=plumbers&find_loc=Los+Angeles%2C+CA'

# Obtener nombres de negocios, URLs y calificaciones
business = get_business(url)
