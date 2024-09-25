from aiogram import types
from loader import dp, bot, db, admin_ids, BOT_DIR
from custom_filters.filters import *
import custom_filters.states as states
from bot_settings import settings_controller
from data.articles_handler import get_all_articles, append_new_articles, save_articles
from wb_parser.photo import update_article_photo
import pandas as pd
import re
import os

@dp.message_handler(IsAdmin(), commands=["start"])
async def on_start_command(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    text = """👋 Привет, я бот по анализу товаров. 
⚙️ Подпишись командой /sub, чтобы получать от меня сообщения об изменениях в товарах.
📋 По команде /help ты узнаешь о дополнительных командах"""
    await bot.send_message(chat_id, text=text)
    db.set_user_state(user_id, user_name=username, state=states.BASE)

@dp.message_handler(IsAdmin(), commands=["add_admin", "remove_admin", "add_vendors", "delete_vendors"])
async def on_main_commands_sending(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    
    text = message.text.strip("/")
    user_state = None
    if text == "add_admin":
        user_state = states.ADD_ADMIN
        await bot.send_message(chat_id, text="Введите id человека, которого вы хотите добавить")
    elif text == "remove_admin":
        user_state = states.REMOVE_ADMIN
        await bot.send_message(chat_id, text="Введите id человека, у которого вы хотите отключить доступ")
    elif text == "add_vendors":
        user_state = states.APPEND_ARTICLES
        await bot.send_message(chat_id, text="Отправьте артикулы через разделитель или xlsx файл, чтобы добавить артикулы")
    elif text == "delete_vendors":
        user_state = states.REMOVE_ARTICLES
        await bot.send_message(chat_id, text="Отправьте артикулы через разделитель или xlsx файл, чтобы удалить ненужные артикулы")
    else:
        user_state = states.BASE
        
    db.set_user_state(user_id, user_name=username, state=user_state)

@dp.message_handler(IsAdmin(), commands=["help"])
async def on_help_command(message: types.Message):
    chat_id = message.chat.id
    commands = {
        "/sub" : "подписаться на рассылку",
        "/unsub" : "отписаться от рассылки",
        "/all_admins" : "показать всех администраторов",
        "/remove_admin" : "удалить администратора",
        "/add_admin" : "добавить администратора",
    }
    text = "Вот все остальные мои команды:\n"
    for command, description in commands.items():
        text += f"{command} - {description}\n"
    text = text.strip("\n")
    await bot.send_message(chat_id, text=text)
    
@dp.message_handler(IsAdmin(), commands=["all_admins"])
async def get_all_admins(message: types.Message):
    chat_id = message.chat.id
    all_users_data = db.get_all_users()
    text = "Вот все администраторы:\n"
    for user in all_users_data:
        user_id = user[0]
        username = "@" + user[1]
        if user_id in admin_ids:
            text += f"{user_id} - {username}\n"
    text = text.strip("\n ")
    await bot.send_message(chat_id, text=text)

    
    
    
@dp.message_handler(IsAdmin(), StateChecker(valid_state=states.ADD_ADMIN, command_priority=True))
async def add_admin(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text.strip(" ,\n")
    if not text.isdigit():
        await bot.send_message(chat_id, text="Айди пользователя должен быть числом")
        return
    new_admin_id = int(text)
    admin_ids.append(new_admin_id)
    settings_controller.add_admin(new_admin_id)
    
    db.set_user_state(user_id, user_name=username, state=states.BASE)
    await bot.send_message(chat_id, text="Пользователь успешно добавлен")
    
@dp.message_handler(IsAdmin(), StateChecker(valid_state=states.REMOVE_ADMIN, command_priority=True))
async def remove_admin(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username 
    text = message.text
    
    if text.isdigit():
        await bot.send_message(chat_id, text="Айди пользователя должен быть числом")
        return
    admin_id = int(text)
    if admin_id not in admin_ids:
        await bot.send_message(chat_id, text="Этот пользователь не является администратором")
        return
    admin_ids.remove(admin_id)
    settings_controller.delete_admin(admin_id)
    
    db.set_user_state(user_id, user_name=username, state=states.BASE)   
    await bot.send_message(chat_id, text="Пользователь успешно удален")



@dp.message_handler(IsAdmin(), StateChecker(valid_state=states.APPEND_ARTICLES, command_priority=True), content_types=types.ContentType.TEXT)
async def append_articles_by_text(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text.strip(" ,\n")

    sent_articles = re.findall(r"[0-9]+", text)
    int_sent_articles = [int(article) for article in sent_articles]
    await _load_articles(chat_id, int_sent_articles) 
    db.set_user_state(user_id=user_id, user_name=username, state=states.BASE)
   
@dp.message_handler(IsAdmin(), StateChecker(valid_state=states.APPEND_ARTICLES, command_priority=True), content_types=types.ContentType.DOCUMENT)
async def append_articles_by_document(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    server_file_path = file.file_path
    file_path = f"{BOT_DIR}/data/{file_id}.xlsx"
    await bot.download_file(file_path=server_file_path, destination=file_path)
    try:
        df = pd.read_excel(file_path)
        sent_articles = df[df.columns[0]].tolist()
        int_sent_articles = [int(art) for art in sent_articles if isinstance(art, int)]
        
    except Exception as err:
        print(err)
        await bot.send_message(chat_id, text="При работе с файлом что-то пошло не так. Попробуйте еще раз!")
        return
    if os.path.exists(file_path):
        os.remove(file_path) 
    await _load_articles(chat_id, int_sent_articles)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.set_user_state(user_id=user_id, user_name=username, state=states.BASE)

async def _load_articles(chat_id, sent_articles: list):
    if not sent_articles or len(sent_articles) == 0:
        await bot.send_message(chat_id, text="Артикулы не найдены, попробуйте еще раз")
        return
    existing_articles = get_all_articles()
    new_articles = []
    for article in sent_articles:
        if article in existing_articles:
            continue
        new_articles.append(article)
    if len(new_articles) == 0:
        if len(sent_articles) == 1:
            await bot.send_message(chat_id, text="Такой артикул уже существуют")
        else:
            await bot.send_message(chat_id, text="Все введенные артикулы уже существуют")
        return
    for new_article in new_articles:
        await update_article_photo(new_article)
    append_new_articles(new_articles)
    await bot.send_message(chat_id, text=f"Получено артикулов - {len(sent_articles)}, из них загружено - {len(new_articles)}")
    
    
    
@dp.message_handler(IsAdmin(), StateChecker(valid_state=states.REMOVE_ARTICLES, command_priority=True), content_types=types.ContentTypes.TEXT)
async def delete_articles_by_text(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text.strip(" ,\n")

    sent_articles = re.findall(r"[0-9]+", text)
    int_sent_articles = [int(art) for art in sent_articles if art.isdigit()]
    await _remove_articles(chat_id, articles_to_remove=int_sent_articles) 
    db.set_user_state(user_id=user_id, user_name=username, state=states.BASE)
    
@dp.message_handler(IsAdmin(), StateChecker(valid_state=states.REMOVE_ARTICLES, command_priority=True), content_types=types.ContentTypes.DOCUMENT)
async def delete_articles_by_document(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    server_file_path = file.file_path
    file_path = f"{BOT_DIR}/data/{file_id}.xlsx"
    await bot.download_file(file_path=server_file_path, destination=file_path)
    try:
        df = pd.read_excel(file_path)
        sent_articles = df[df.columns[0]].tolist()
        int_sent_articles = [art for art in sent_articles if isinstance(art, int)]
    except Exception as err:
        print(err)
        await bot.send_message(chat_id, text="При работе с файлом что-то пошло не так. Попробуйте еще раз!")
        return 
    if os.path.exists(file_path):
        os.remove(file_path)
    await _remove_articles(chat_id, articles_to_remove=int_sent_articles)
    db.set_user_state(user_id=user_id, user_name=username, state=states.BASE)
    
async def _remove_articles(chat_id, articles_to_remove: list):
    if not articles_to_remove or len(articles_to_remove) == 0:
        await bot.send_message(chat_id, text="Артикулы не найдены, попробуйте еще раз")
        return
    existing_articles = get_all_articles()
    valid_articles = [art for art in existing_articles if art not in articles_to_remove]
    deleted_articles_count = len(existing_articles) - len(valid_articles)
    if deleted_articles_count == 0:
        await bot.send_message(chat_id, text="Не один артикул не был удален")
    else:
        db.delete_products(articles_to_remove)
        save_articles(all_articles=valid_articles)
        await bot.send_message(chat_id, text=f"Операция успешно завершена, удалено артикулов - {deleted_articles_count} из {len(articles_to_remove)}")
    
