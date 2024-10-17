import aiohttp
import aiofiles
import asyncio
import os
from loader import BOT_DIR
from data.articles_handler import get_all_articles
from wb_parser.common import get_session, get_basket
import logging

UPDATE_WAITING_TIME_SECONDS = 10 * 3600
PHOTO_DIR = f"{BOT_DIR}/data/photo"

async def regular_all_photo_update():
    while True:
        all_articles = get_all_articles()
        session = get_session()
        for article in all_articles:
            await update_article_photo(article, session=session)
        await session.close()
        
        #delete photo from not existing articles

        for photo_file_name in os.listdir(PHOTO_DIR):
            try:
                photo_article = int(photo_file_name.split(".")[0])
                if photo_article not in all_articles:
                    photo_path = f"{PHOTO_DIR}/{photo_file_name}"
                    os.remove(photo_path)
            except:
                continue                
        await asyncio.sleep(UPDATE_WAITING_TIME_SECONDS)
    
async def update_article_photo(article: int, session: aiohttp.ClientSession = None):
    is_local_session = False
    basket_url = get_basket(article)
    main_img_url = f'{basket_url}/images/big/1.webp'
    img_path = f"{PHOTO_DIR}/{article}.webp"
    if not session:
        session = get_session()
        is_local_session = True
    if os.path.exists(img_path):
        os.remove(img_path)
    tryings = 5
    for i in range(tryings):
        try:
            async with session.get(main_img_url) as response:
                if response.status != 200:
                    logging.error(f"{article} - photo getting status != 200")
                    continue
                content = await response.read()
                async with aiofiles.open(img_path, "wb") as photo:
                    await photo.write(content)
                logging.warning(f"{article} - successfully")
                break
        except Exception as err:
            logging.exception(f"{article} - photo exception")
            # if os.path.exists(img_path):
            #     os.remove(img_path)
        finally:
            await asyncio.sleep(30)
    else:
        logging.error(f"{article} - photo dont get")
    if is_local_session:
        await session.close()

