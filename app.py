import requests
from bs4 import BeautifulSoup

def get_profile_data(profile_url):
    response = requests.get(profile_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        logo_class = soup.find('img', class_='businessLogo__09f24__jydFo businessLogo--v2__09f24__MfF2g')
        logo = 'No' if not logo_class else 'Yes'

        portfolios = soup.find_all('h2', class_='css-13merx8')
        portfolio = 'No'
        for item in portfolios:
            if 'Portfolio from the Business' in item.text:
                portfolio = 'Yes'
                break

        highlights_container = soup.find('div', class_='arrange__09f24__LDfbs gutter-2__09f24__CCmUo layout-wrap__09f24__GEBlv layout-6-units__09f24__pP1H0 css-1qn0b6x')
        highlights = [span.get_text() for span in highlights_container.find_all('span', class_='mobile-text-medium__09f24__MZ1v6 css-1dtv2dz')] if highlights_container else 'No'

        get_price = 'Yes' if soup.find('button', class_='css-1ru1z96') else 'No'

        rate_class = 'css-1p9ibgf'
        rate_element = soup.find('span', class_=rate_class)
        reviews_container = soup.find_all('div', class_='css-1qn0b6x')
        reviews = [{'text': review.find('p', class_='comment__09f24__D0cxf css-qgunke').get_text(), 'date': review.find('span', class_='css-chan6m').get_text()} for review in reviews_container if review.find('p', class_='comment__09f24__D0cxf css-qgunke') and review.find('span', class_='css-chan6m')]

        web_and_phone_class = 'arrange__09f24__LDfbs gutter-2__09f24__CCmUo vertical-align-middle__09f24__zU9sE css-1qn0b6x'
        web_and_phone_elements = soup.find_all('div', class_=web_and_phone_class)

        web_found, phone_found = False, False
        phone, web = None, None

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
                    break

        if rate_element:
            rate_text = rate_element.text.strip()
            rate_value = float(rate_text.split()[0])
            return rate_value, reviews, phone, web, get_price, highlights, portfolio, logo
        else:
            return None, None, None, None, None, None, None, None
    else:
        return None, None, None, None, None, None, None, None

def get_business(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        negocios = []
        business_container_class = 'container__09f24__FeTO6 hoverable__09f24___UXLO css-azqg3k'
        businesses = soup.find_all('div', class_=business_container_class)

        for business in businesses[:10]:
            business_name_element = business.find('a', class_='css-19v1rkv')
            if business_name_element:
                business_name_text = business_name_element.text.strip()
                business_href = business_name_element['href']
                full_url = 'https://www.yelp.com' + business_href

                response_time_element = business.find('span', {'class': ['raqResponseTime', 'raqFastResponder']})
                response_time = response_time_element.text.strip() if response_time_element else 'No response time'

                verified_license_element = business.find('span', class_='css-11pkcdj')
                has_verified_license = 'Yes' if verified_license_element and 'Verified License' in verified_license_element.text else 'No'

                rate, reviews, phone, website, get_price, highlights, portfolio, logo = get_profile_data(full_url)

                if rate is not None:
                    last_3_reviews = reviews[-3:]

                    negocios.append({
                        'name': business_name_text,
                        'href': full_url,
                        'rate': rate,
                        'logo': logo,
                        'get_price': get_price,
                        'portfolio': portfolio,
                        'highlights': highlights,
                        'phone': phone,
                        'website': website,
                        'response_time': response_time,
                        'reviews': last_3_reviews
                    })
        return negocios
    else:
        return None

url = 'https://www.yelp.com/search?find_desc=plumbers&find_loc=Los+Angeles%2C+CA'
businesses_list = get_business(url)

# Imprimir la lista de negocios
for business in businesses_list:
    print(business)
