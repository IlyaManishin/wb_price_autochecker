from aiogram import types
from loader import dp, bot, db, BOT_DIR
from custom_filters.filters import *
import custom_filters.states as states

import pandas as pd
from openpyxl import Workbook
import re
import os
import aiofiles


@dp.message_handler(IsAdmin(), commands=["all_vendors"])
async def get_all_vendors(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.username
    
    vendors_file_path = f"{BOT_DIR}/data/articles.xlsx"
    vendors_df = pd.read_excel(vendors_file_path, sheet_name="Лист1")   
    data = vendors_df.to_dict("split")
    vendors = [i[0] for i in data["data"]]
    
    temp_vendors_file_path = f"{BOT_DIR}/data/articles_temp.xlsx"
    if os.path.exists(path=temp_vendors_file_path):
        os.remove(temp_vendors_file_path)
    wb = Workbook()
    wb.save(temp_vendors_file_path)
    temp_vendors_df = pd.DataFrame(columns=["Артикулы", "Ссылка"])
    for vendor in vendors:
        row = [vendor, f"https://www.wildberries.ru/catalog/{vendor}/detail.aspx"]
        temp_vendors_df.loc[len(temp_vendors_df)] = row
    temp_vendors_df.to_excel(temp_vendors_file_path, sheet_name="Лист1", index=False)
    
    async with aiofiles.open(temp_vendors_file_path, "rb") as data:
        # data = await file.read()
        await bot.send_message(chat_id, text="Вот ваш файл:")
        await bot.send_document(chat_id, document=data)
    db.set_user_state(user_id, user_name, state=states.BASE)
    if os.path.exists(temp_vendors_file_path):
        os.remove(temp_vendors_file_path)
    
