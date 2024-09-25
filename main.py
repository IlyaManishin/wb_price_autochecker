from aiogram import executor, types
import asyncio


async def on_startup(dp):
    from custom_filters.filters import IsAdmin, StateChecker
    
    dp.filters_factory.bind(IsAdmin, event_handlers=[dp.message_handlers])
    dp.filters_factory.bind(StateChecker, event_handlers=[dp.message_handlers])
    
    from loader import bot
    bot_commands = [
        types.BotCommand(command="/sub", description="Подписка на рассылку"),
        types.BotCommand(command="/help", description="Помощь"),
        types.BotCommand(command="/add_vendors", description="Добавить артикулы"),
        types.BotCommand(command="/delete_vendors", description="Удалить артикулы"),
        types.BotCommand(command="/all_vendors", description="Выгрузить все артикулы"),
    ]
    await bot.set_my_commands(bot_commands)
    from wb_parser.photo import regular_all_photo_update
    from wb_parser.destribution import regular_destribution
    
    asyncio.create_task(regular_all_photo_update())
    asyncio.create_task(regular_destribution())
    
if __name__ == "__main__":
    from loader import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)