from aiogram import types
from loader import dp, bot, chat_ids_for_distribution
from custom_filters.filters import *
from bot_settings import settings_controller


@dp.message_handler(IsAdmin(), commands=["sub", "unsub"])
async def sub_or_unsub_on_distribution(message: types.Message):
    chat_id = message.chat.id
    text = message.text
    if "/sub" in text:
        if chat_id not in chat_ids_for_distribution:
            chat_ids_for_distribution.append(chat_id)
            settings_controller.add_chat_id_for_distribution(chat_id)
            await bot.send_message(chat_id, text="Вы подписались на рассылку")
        else:
            await bot.send_message(chat_id, text="Вы уже подписаны на рассылку")
    elif "/unsub" in text:
        if chat_id in chat_ids_for_distribution:
            chat_ids_for_distribution.remove(chat_id)
            settings_controller.delete_chat_id_for_distribution(chat_id)
            await bot.send_message(chat_id, text="Вы успешно отписались от рассылки")
        else:
            await bot.send_message(chat_id, text="Вы уже отписаны от рассылки")
    else:
        await bot.send_message(chat_id, text="Непредвиденная ошибка")

