import requests
from bs4 import BeautifulSoup

def get_profile_highlights(profile_url):
    response = requests.get(profile_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        highlights_container = soup.find('div', class_='arrange__09f24__LDfbs gutter-2__09f24__CCmUo layout-wrap__09f24__GEBlv layout-6-units__09f24__pP1H0 css-1qn0b6x')

        highlights = []
        if highlights_container:
            spans = highlights_container.find_all('span', class_='mobile-text-medium__09f24__MZ1v6 css-1dtv2dz')
            for span in spans:
                highlight_text = span.get_text()
                highlights.append(highlight_text)

        if not highlights:  # Si la lista está vacía
            return 'No'
        else:
            return highlights
    else:
        print(f"No se pudo obtener la página del perfil. Código de estado: {response.status_code}")
        return None

url = "https://www.yelp.com/biz/fix-it-quick-plumbing-canoga-park-2?override_cta=Get+pricing+%26+availability"
url2 = "https://www.yelp.com/biz/tejedas-plumbing-rosemead?osq=plumbers&override_cta=Get+pricing+%26+availability"
print(f'highlights: {get_profile_highlights(url)}')
