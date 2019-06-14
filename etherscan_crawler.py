import requests
import threading
from bs4 import BeautifulSoup
from datetime import datetime
from queue import Queue


def get_trans(txn_hash, q=None):
    """
    取得單一交易紀錄
    :param q: 裝結果的容器
    :param txn_hash: 交易編號
    :return: 回傳單一交易紀錄dict
    """
    url = f'https://etherscan.io/tx/{txn_hash}'

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'lxml')

    result = {}
    # transaction_hash
    result['transaction_hash'] = txn_hash

    # block block_confirmations
    confirmation_text = soup.find(class_='u-label u-label--xs u-label--badge-in u-label--secondary ml-1').text
    iEnd = confirmation_text.find(' ')
    result['block_confirmations'] = int(confirmation_text[0:iEnd])

    # timestamp
    time_str = soup.find_all('div', class_='row align-items-center')[1].find('div', class_='col-md-9').text
    time_str = time_str[time_str.find('(') + 1:time_str.find(')')]
    datetime_object = datetime.strptime(time_str, '%b-%d-%Y %H:%M:%S %p +%Z')
    result['timestamp'] = str(datetime_object)

    # from
    result['from'] = soup.find(id='addressCopy').text

    # to
    result['to'] = soup.find(id='contractCopy').text

    # value
    result['value'] = soup.find('div', class_='media-body').find_all('span', class_='mr-1')[-1].text.strip()

    # set result to queue(if q)
    if q:
        q.put(result)
        print(f'{txn_hash}:ok')
    return result


def get_trans_txn_hash_list(page):
    """
    取得第page頁交易紀錄中的txn_hash列表
    :param page: 頁數
    :return: 回傳該頁txn_hash的list
    """
    params = {
        'contractAddress': '0xdac17f958d2ee523a2206206994597c13d831ec7',
        'p': page
    }

    url = f'https://etherscan.io/token/generic-tokentxns2'

    r = requests.get(url, params=params)

    soup = BeautifulSoup(r.text, 'lxml')

    result = []
    for tr in soup.find_all('tr'):
        try:
            result.append(tr.find_all('td')[0].text)
        except IndexError:
            pass
    return result


def get_trans_list(page):
    """
    取得第page頁交易紀錄列表
    :param page: 頁數
    :return: 回傳該頁交易紀錄dict的list
    """
    result = []

    for txn_hash in get_trans_txn_hash_list(page):
        trans = get_trans(txn_hash)
        result.append(trans)
    return result


def async_get_trans_list(page):
    """
    取得第page頁交易紀錄列表
    :param page: 頁數
    :return: 回傳該頁交易紀錄dict的list
    """
    q = Queue()
    threads = []

    # execute func 'get_trans' async
    trans_txn_hash_list = get_trans_txn_hash_list(page)
    for txn_hash in trans_txn_hash_list:
        t = threading.Thread(target=get_trans, args=(txn_hash, q))
        t.start()
        threads.append(t)

    # wait all thread
    for t in threads:
        t.join()

    # set results
    results = []
    for i in range(len(trans_txn_hash_list)):
        results.append(q.get())

    return results
