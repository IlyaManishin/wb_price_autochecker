import asyncio
import json
import aiohttp
from aiohttp.web import HTTPException
from loader import db
from data.articles_handler import get_all_articles
from wb_parser.common import get_session, get_basket


async def get_all_products_data():
    all_articles = get_all_articles()
    session = get_session()
    all_products_data = []
    wallet = await get_wallet_percent()
    for article in all_articles:
        data = await get_product_data(article, session, wallet)
        if not data:
            continue
        if not data["base-price"]:
            continue
        all_products_data.append(data)
    await session.close()
    return all_products_data
    

async def get_product_data(article: int, session: aiohttp.ClientSession, wallet: int):
    data = {
        "article" : article,
        "seller" : None,
        "base-price" : None,
        "wallet_price" : 0,
        "wallet" : wallet,
    }
    product_url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=40&nm={article}"
    #иногда вб блокает доступ, нужно несколько попыток
    tryings = 3
    for i in range(tryings):
        try:
            async with session.get(product_url) as response:
                text = await response.text()
                all_data = json.loads(text)
                product = all_data["data"]["products"][0]
                try:
                    price_retail = product["priceU"] // 100
                except:
                    price_retail = 0
                try:
                    full_sale = product["sale"]
                except:
                    full_sale = 0
                    
                try:
                    spp_price = product["salePriceU"] // 100
                except:
                    spp_price = 0
                
                try:
                    wallet_price = int(spp_price * ((100-wallet)/100))
                except:
                    wallet_price = 0
                

                data["base-price"] = price_retail
                data["spp-price"] = spp_price
                data["wallet_price"] = wallet_price
                break
                        
        except HTTPException as err:
            print(err)
            await asyncio.sleep(10)
            continue
        except Exception as err:
            break
    else:
        #если 3 раза ошибка и результата нет
        return None

    try:
        basket = get_basket(article)
        seller_url = f"{basket}/info/sellers.json"
        async with session.get(seller_url) as response:
            text = await response.text()
            seller_info = json.loads(text)
            if "supplierName" in seller_info:
                data["seller"] = seller_info["supplierName"]
    except:
        pass
    return data
    
async def get_wallet_percent():
    tryings = 5
    session = aiohttp.ClientSession()
    url = "https://static-basket-01.wbbasket.ru/vol0/data/settings-front-ru.json"
    percent = None
    for i in range(tryings):
        try:
            async with session.get(url=url) as resp:
                text = await resp.text()
                data = json.loads(text)
                percent = int(data["variables"]["wlt1DiscountPercent"])
                break
        except:
            pass
    await session.close()
    if not percent:
        return 0
    return percent