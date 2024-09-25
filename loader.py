import os
from aiogram import Bot, Dispatcher
from bot_settings import settings_controller as sett_contr
import custom_filters.states as states
import logging

ALL_COMMANDS = ["/start", "/help", "/all_admins", "/add_admin", "/remove_admin", "/add_vendors", "/delete_vendors", "/all_vendors", "/sub", "/unsub"]
BOT_DIR = os.path.dirname(os.path.realpath(__file__))
TABLE_PATH = f"{BOT_DIR}/data/table.db"

logging.basicConfig(filename=f"{BOT_DIR}/data/logger.log", 
                    level=logging.INFO, 
                    filemode="a", 
                    encoding="utf-8", 
                    format=r"%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

bot_token = sett_contr.get_bot_token()
admin_ids: list = sett_contr.get_admins()
chat_ids_for_distribution: list = sett_contr.get_chat_ids_for_distribution()

bot = Bot(bot_token)
dp = Dispatcher(bot)

from data.sqlite_controller import SqliteTable
db = SqliteTable(table_path=TABLE_PATH)

from handlers import *




