import requests
from bs4 import BeautifulSoup


def get_confirmation_count(tx_id):
    url = "https://etherscan.io/tx/" + tx_id

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'lxml')
    span = soup.find(class_='u-label u-label--xs u-label--badge-in u-label--secondary ml-1')
    confirmation_text = span.text
    iEnd = confirmation_text.find(' ')
    return int(confirmation_text[0:iEnd])


print(get_confirmation_count('your_tx_id'))
