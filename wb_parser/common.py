import aiohttp

HEADERS = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'dnt': '1',
    'origin': 'https://www.wildberries.ru',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Safari/537.36',
}

def get_session() -> aiohttp.ClientSession:
    connector = aiohttp.TCPConnector(limit=500)
    session_timeout = aiohttp.ClientTimeout(total=60)
    session = aiohttp.ClientSession(headers=HEADERS, timeout=session_timeout, connector=connector) 
    return session

def get_basket(article):
    vol = int(article / 100000)
    part = int(article / 1000)
    
    if vol <= 143:
        basket = f"https://basket-01.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 287:
        basket = f"https://basket-02.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 431:
        basket = f"https://basket-03.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 719:
        basket = f"https://basket-04.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 1007:
        basket = f"https://basket-05.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 1061:
        basket = f"https://basket-06.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 1115:
        basket = f"https://basket-07.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 1169:
        basket = f"https://basket-08.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 1313:
        basket = f"https://basket-09.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 1601:
        basket = f"https://basket-10.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 1655:
        basket = f"https://basket-11.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 1919:
        basket = f"https://basket-12.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 2045:
        basket = f"https://basket-13.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 2189:
        basket = f"https://basket-14.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 2405:
        basket = f"https://basket-15.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 2621:
        basket = f"https://basket-16.wbbasket.ru/vol{vol}/part{part}/{article}"
    elif vol <= 2837:
        basket = f"https://basket-17.wbbasket.ru/vol{vol}/part{part}/{article}"
    else:
        basket = f"https://basket-18.wbbasket.ru/vol{vol}/part{part}/{article}"
                                                        
    return basket
    
    