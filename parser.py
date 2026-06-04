import requests
from bs4 import BeautifulSoup
import time

result = []

for _ in range(15):

    resp = requests.get('https://coinmarketcap.com/')

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text , features='html.parser')

        soup_list = soup.find_all('div', {'class': 'sc-631098c-0'})

        bitcoin = soup_list[1].find('span').text
        ethereum = soup_list[2].find('span').text

        print(f'Курс біткоіна: {bitcoin}')
        print(f'Курс ефіру: {ethereum}')
        result.append(bitcoin)
        time.sleep(10)

print(*result, sep='\n')

