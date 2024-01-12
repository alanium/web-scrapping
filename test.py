import requests
from bs4 import BeautifulSoup


def get_profile_data(profile_url):
    # Hacer una solicitud HTTP a la página del perfil de Yelp
    response = requests.get(profile_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar botones con la clase css-1ru1z96
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

        return get_price


url = "https://www.yelp.com/biz/charlies-sewer-and-drain-rooter-company-north-hollywood?override_cta=Get+pricing+%26+availability"
url2 = "https://www.yelp.com/biz/new-generation-plumbing-los-angeles-4?override_cta=Get+pricing+%26+availability"

print(get_profile_data(url2))