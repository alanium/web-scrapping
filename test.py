import requests
from bs4 import BeautifulSoup

def get_profile_highlights(profile_url):
    response = requests.get(profile_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        portfolios = soup.find_all('span', class_='css-11pkcdj')
        portfolio = 'No'

        for item in portfolios[:5]:
            if 'Verified License' in item.text:
                portfolio = 'Yes'
            else:
                print(portfolio)

        return portfolio

url_yes = "https://www.yelp.com/search?find_desc=plumbers&find_loc=Los+Angeles%2C+CA"

print(get_profile_highlights(url_yes))
