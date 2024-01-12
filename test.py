import requests
from bs4 import BeautifulSoup

def get_profile_highlights(profile_url):
    response = requests.get(profile_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        logo_class = soup.find('img', class_='businessLogo__09f24__jydFo businessLogo--v2__09f24__MfF2g')
        logo = 'No'

        if logo_class:
            logo = 'Yes'

        return logo

url_yes = "https://www.yelp.com/biz/fix-it-quick-plumbing-canoga-park-2?override_cta=Get+pricing+%26+availability"
url_not = "https://www.yelp.com/biz/tejedas-plumbing-rosemead?osq=plumbers&override_cta=Get+pricing+%26+availability"

print(f'Response Yes: {get_profile_highlights(url_yes)}')
print(f'Response No: {get_profile_highlights(url_not)}')
