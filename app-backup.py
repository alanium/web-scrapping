import requests
from bs4 import BeautifulSoup
import time
import random
from flask import Flask, render_template, request

app = Flask(__name__)

def get_profile_data(profile_url):

    # Agrega una demora aleatoria entre 1 y 10 segundos
    time.sleep(random.uniform(1, 10))

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Agrega una demora aleatoria entre 1 y 10 segundos
    time.sleep(random.uniform(1, 10))

    response = requests.get(url, headers=headers)
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


                if reviews:
                    last_3_reviews = reviews[-3:]
                else:
                    last_3_reviews = []

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
                    'has_verified_license': has_verified_license,
                    'reviews': last_3_reviews
                })
        return negocios
    else:
        return None

"""url = 'https://www.yelp.com/search?find_desc=plumbers&find_loc=Los+Angeles%2C+CA'
businesses_list = get_business(url)

# Imprimir la lista de negocios
for business in businesses_list:
    print(business)"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.form['url']
    #businesses_list = get_business(url)

    businesses_list = [{'name': 'Tankless Water Heater Repair and Plumbing', 'href': 'https://www.yelp.com/adredir?ad_business_id=2gn5VC71VrbcAhPRylOx-w&campaign_id=FeKuD0I0vJlCexkmC_g2Xw&click_origin=search_results&placement=vertical_0&placement_slot=1&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Ftankless-water-heater-repair-and-plumbing-los-angeles%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=d4e37bfbbd32b08fd9c07e5bdda273e8dab9be3da746c0f1d118a06f478be30a&slot=0', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': 'No response time', 'has_verified_license': 'Yes', 'reviews': []}, {'name': 'New Generation Plumbing', 'href': 'https://www.yelp.com/adredir?ad_business_id=XDL-HZalFLuBZNGtwBAj5w&campaign_id=1aqF80mAQJKcuK-obj7krw&click_origin=search_results&placement=vertical_0&placement_slot=1&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Fnew-generation-plumbing-los-angeles-4%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=70b28cad6eec87102e0e77e1fa2a45361399c66497da417743ef889e070603e7&slot=1', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': '10 minutes', 'has_verified_license': 'Yes', 'reviews': []}, {'name': 'Pro Quality Plumbing', 'href': 'https://www.yelp.com/adredir?ad_business_id=n8mvCwCXDSC7TCXmqi6ynA&campaign_id=jU6IFHLgq7r93nSX-kLbsA&click_origin=search_results&placement=vertical_0&placement_slot=1&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Fpro-quality-plumbing-simi-valley-4%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=4581752de181bd00beea8c52fdce4927d4a0bdfff3ad10c131901e8f3a45cc14&slot=2', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': '10 minutes', 'has_verified_license': 'Yes', 'reviews': []}, {'name': 'Honest Rooter Services', 'href': 'https://www.yelp.com/adredir?ad_business_id=Er-nbYbtvFBEvldkBlHU6w&campaign_id=o6DCDTul7t6t3QdbJmHJ0g&click_origin=search_results&placement=vertical_0&placement_slot=1&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Fhonest-rooter-services-west-hollywood%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=b87c2a19110d35bbe5464de93be7db1fbaefdbc7421f9a6f4d9dee491e2127cc&slot=3', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': 'No response time', 'has_verified_license': 'No', 'reviews': []}, {'name': 'Team Rooter Plumbing', 'href': 'https://www.yelp.com/adredir?ad_business_id=lQaQc2-SZbhPuJ7qz2kSQw&campaign_id=Wz4MXEIZHhsSR6VrGqCvlg&click_origin=search_results&placement=vertical_0&placement_slot=1&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Fteam-rooter-plumbing-simi-valley%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=3c2d84e8242af5c9aa4036c915c0d9918e6d0aa8387928efc9928c24c8cb8edf&slot=4', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': '20 minutes', 'has_verified_license': 'Yes', 'reviews': []}, {'name': 'American Drain Company', 'href': 'https://www.yelp.com/adredir?ad_business_id=Kc83H_bsP7CkSpwi40dQ9Q&campaign_id=HAC3Yp-rQazDLEhjjRpYhw&click_origin=search_results&placement=vertical_0&placement_slot=1&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Famerican-drain-company-simi-valley-5%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=e99943cc4539547fd4dfa2f8846e661cef081867bd21018e1f95ebb9e0033f6d&slot=5', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': 'No response time', 'has_verified_license': 'Yes', 'reviews': []}, {'name': 'Velocity Rooter & Plumbing Services', 'href': 'https://www.yelp.com/adredir?ad_business_id=h921uL9Taobzmcbt24maMw&campaign_id=YulD0sZ1wMtArBZ6KzL6Tg&click_origin=search_results&placement=vertical_0&placement_slot=1&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Fvelocity-rooter-and-plumbing-services-los-angeles%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=5a8a5dcadef1f30947e08ede5fe75fae0b397e3831b97596e1063896a8f744d4&slot=6', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': '10 minutes', 'has_verified_license': 'No', 'reviews': []}, {'name': 'JA Plumbing', 'href': 'https://www.yelp.com/adredir?ad_business_id=3bEyPYbFGqBsQmsRtsuaiw&campaign_id=LDHXEBPUO6eHeoZUyGVF7Q&click_origin=search_results&placement=vertical_1&placement_slot=3&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Fja-plumbing-los-angeles%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=f735481ae85770935ae9044a025274d3032fba477b3555e3fbaac5cefd28f409&slot=0', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': 'No response time', 'has_verified_license': 'Yes', 'reviews': []}, {'name': 'NexGen HVAC & Plumbing', 'href': 'https://www.yelp.com/adredir?ad_business_id=BpMfCxBbcSynCbM5GDa6UQ&campaign_id=jaokkfsTkF-_rQD5dxXSWQ&click_origin=search_results&placement=vertical_1&placement_slot=3&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Fnexgen-hvac-and-plumbing-arcadia%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=fd2fbc60af955ffef7c9f2d3caf9363734740690b40d4ae6c6726255df2cd46d&slot=1', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': '10 minutes', 'has_verified_license': 'Yes', 'reviews': []}, {'name': 'Kurt Bohmer’s Plumbing & Drain Service', 'href': 'https://www.yelp.com/adredir?ad_business_id=-J6jJ_ZqdksxGz_zgOh4Kg&campaign_id=jN5h2LcjD_LQP9SHPrWGbg&click_origin=search_results&placement=vertical_1&placement_slot=3&redirect_url=https%3A%2F%2Fwww.yelp.com%2Fbiz%2Fkurt-bohmers-plumbing-and-drain-service-palmdale%3Foverride_cta%3DGet%2Bpricing%2B%2526%2Bavailability&request_id=f488dc9eb34c8e92&signature=996a36c7408d98985ec8869a1b8ee5b024b4a55058d1d11c311996f7ed3afa1d&slot=2', 'rate': None, 'logo': None, 'get_price': None, 'portfolio': None, 'highlights': None, 'phone': None, 'website': None, 'response_time': 'No response time', 'has_verified_license': 'Yes', 'reviews': []}]


    if businesses_list:
        return render_template('result.html', businesses=businesses_list)
    else:
        return "No se pudieron obtener datos. Verifica la URL e inténtalo de nuevo."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)