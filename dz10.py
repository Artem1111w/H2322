import requests
from bs4 import BeautifulSoup
import time

result = []

for _ in range(15):

    resp = requests.get('https://bank.gov.ua/')

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text , features='html.parser')

        soup_list = soup.find_all('div', {'class': 'value index-page'})

        #usd = soup_list[2].text
        #euro = soup_list[2].text

        print(f'Курс Долара: {soup_list[3].text.strip()}')
        print(f'Курс Евро: {soup_list[2].text.strip()}')
        #result.append(usd)
        time.sleep(10)

print(*result, sep='\n')

