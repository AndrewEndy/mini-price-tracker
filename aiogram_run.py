import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from apscheduler.triggers.interval import IntervalTrigger
from app.bot.create_bot import bot, dp, scheduler, admins
from app.services import check_products_updates

#from work_time.send_message import send_message_time
from datetime import datetime, timedelta

from app.bot.handlers.user_handler import user_router
from app.bot.handlers.view_products_handler import view_router
from app.bot.handlers.update_product_handler import update_product_data_router
from app.bot.handlers.delete_product_handler import delete_product_router
from app.bot.handlers.add_product_handler import add_product_router


async def set_commands():
    commands = [BotCommand(command='start', description='Запустити/перезапустити бота'),
                BotCommand(command='info', description='Інформація про бот'),
                BotCommand(command='menu', description='Повернутись на головне меню')
                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())



async def start_bot():
    await set_commands()
        
    #count_users = await get_all_users(count=True)
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, f'Я запущений🥳')
    except:
        pass
    await check_products_updates()

# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот виключений😔')
    except:
        pass



async def main():
    scheduler.add_job(
        check_products_updates,  # Ваша функція
        IntervalTrigger(hours=12),  # Триггер для виконання кожні 12 годин
        name="Check prices every 12 hours",
    )

#     scheduler.add_job(
#         check_products_updates,  # Ваша функція
#         IntervalTrigger(minutes=1),  # Триггер для тесту (кожну хвилину)
#         name="Check prices every minute (test)",
#     )

    scheduler.start()
    
    dp.include_router(user_router)
    dp.include_router(view_router)
    dp.include_router(update_product_data_router)
    dp.include_router(delete_product_router)
    dp.include_router(add_product_router)
    
    
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'\033[32mБот завершив роботу\033[0m')




# TODO: пофіксити загальну зміну, всьо ше раз перевірити, Закомітити