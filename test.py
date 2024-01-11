import requests
from bs4 import BeautifulSoup

url = "https://www.yelp.com/biz/fix-it-quick-plumbing-canoga-park-2?override_cta=Get+pricing+%26+availability"


# Realizar la solicitud HTTP y obtener el contenido de la página
response = requests.get(url)
html_content = response.text

# Utilizar BeautifulSoup para analizar el HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar la sección que contiene el teléfono y la página web
web_and_phone_class = 'arrange__09f24__LDfbs gutter-2__09f24__CCmUo vertical-align-middle__09f24__zU9sE css-1qn0b6x'
web_and_phone_elements = soup.find_all('div', class_=web_and_phone_class)

web_found = False

if web_and_phone_elements:
    for element in web_and_phone_elements:
        text_element = element.find('p', class_='css-1p9ibgf')
        if text_element:
            text = text_element.text.strip()
            if not web_found:
                print(f'Business website: {text}')
                web_found = True
            else:
                print(f'Phone number: {text}')
                break  # Salir del bucle después de encontrar el número
else:
    print('Business website and Phone number not found on the profile page.')
