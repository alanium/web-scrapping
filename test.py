import requests
from bs4 import BeautifulSoup

url = "https://www.yelp.com/biz/charlies-sewer-and-drain-rooter-company-north-hollywood?override_cta=Get+pricing+%26+availability"

# Realizar la solicitud HTTP y obtener el contenido de la página
response = requests.get(url)
html_content = response.text

# Utilizar BeautifulSoup para analizar el HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Buscar botones con la clase css-1ru1z96
buttons = soup.find_all('button', class_='css-1ru1z96')

if buttons:
    for button in buttons:
        span_inside_button = button.find('span', class_='css-1enow5j')
        if span_inside_button:
            print(f'Get pricing & availability: Yes')
        else:
            print('No se encontró span dentro del botón.')
else:
    print('No se encontró el botón.')

