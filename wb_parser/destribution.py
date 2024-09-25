import asyncio
import time
import aiohttp
import aiofiles
import os
from loader import db, bot, chat_ids_for_distribution
from wb_parser.product_data import get_all_products_data
from wb_parser.photo import PHOTO_DIR

WAITING_TO_DESTRIBUTION_SEC = 4 * 60

async def regular_destribution():
    while True:
        time_in_start = time.time()
        all_product_data = await get_all_products_data()
        for product_data in all_product_data:
            article = product_data["article"]
            last_product_data = db.get_product_data(article)
            if not last_product_data:
                db.add_product(product_data)
                continue
            if product_data["spp-price"] == last_product_data["spp-price"] and product_data["wallet_price"] == last_product_data["wallet_price"]:
                continue
            await notify_about_changes(article=article,
                                        now_product_data=product_data,
                                        last_product_data=last_product_data)
            db.update_product(product_data)
        time_in_finish = time.time()
        execution_time = time_in_finish - time_in_start
        print(f"Execute time = {round(execution_time/60, 1)} min")
        sleep_time = WAITING_TO_DESTRIBUTION_SEC - execution_time
        min_sleep_time = WAITING_TO_DESTRIBUTION_SEC // 2
        if sleep_time < min_sleep_time:
            sleep_time = min_sleep_time
        await asyncio.sleep(sleep_time)
    
                
        
async def notify_about_changes(article: int, now_product_data: dict, last_product_data: dict):
    is_photo_exists = False
    photo_path = f"{PHOTO_DIR}/{article}.jpg"
    if os.path.exists(photo_path):
        is_photo_exists = True
    text = ""
    if now_product_data["seller"]:
        text += f"Продавец: {now_product_data['seller']}\n\n"
    article_url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
    article_url_tag = f'<a href="{article_url}">{article}</a>'
    text += f"У товара с артикулом {article_url_tag} изменилась цена\n"
    text += f"Копировать: <code>{article}</code>\n\n"
    # text += "Цена от продавца:\n"
    # text += get_description_by_compare(last_product_data["base-price"], now_product_data["base-price"], postfix="₽")
    # text += "\n\n"
    
    # text += "СПП (WB скидка):\n"
    # text += get_description_by_compare(last_product_data["spp"], now_product_data["spp"], postfix="%")
    # text += "\n\n"

    text += "Цена для клиента (с СПП):\n"
    text += get_description_by_compare(last_product_data["spp-price"], now_product_data["spp-price"], postfix="₽")
    text += "\n\n"

    text += f"Цена с WB кошельком ({now_product_data['wallet']}%):\n"
    text += get_description_by_compare(last_product_data["wallet_price"], now_product_data["wallet_price"], postfix="₽")
        
    for chat_id in chat_ids_for_distribution:
        try:
            if is_photo_exists:
                async with aiofiles.open(photo_path, "rb") as photo:
                    data = await photo.read()
                    await bot.send_photo(chat_id, photo=data, caption=text, parse_mode="HTML")
            else:
                await bot.send_message(chat_id, text=text, parse_mode="HTML")
        except Exception as err:
            print(err)
            print(article)
            print(f"cant notify chat_id = {chat_id}")
        finally:
            await asyncio.sleep(0.4)
    
def get_description_by_compare(last, now, postfix) -> str:
    stickers = {"less" : "⬇️", "more" : "⬆️", "equals" : ""}
    text = ""
    if not last or not now:
        sticker = stickers["equals"]
        if not last:
            text += f"Было: нет данных\n"
        else:
            text += f"Было: {last}{postfix}\n"
            
        if not now:
            text += f"Стало: нет данных {sticker}"
        else:
            text += f"Стало: {now}{postfix} {sticker}"
    else:
        if now > last:
            sticker = stickers["more"]
        elif now < last:
            sticker = stickers["less"]
        else:
            sticker = stickers["equals"]
        text += f"Было: {last}{postfix}\n"
        text += f"Стало: {now}{postfix} {sticker}"
    return text