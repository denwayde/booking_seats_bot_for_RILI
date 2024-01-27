import asyncio
from aiogram import Bot, Dispatcher
# from config_handler import settings
from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных из файла .env


bot_key = os.getenv('BOT_TOKEN')
payment_key = os.getenv('PAYMENT_TOKEN')   



# Запуск бота
async def main():
    bot = Bot(token=bot_key)
    dp = Dispatcher()

    # Запускаем бота и пропускаем все накопленные входящие
    # Да, этот метод можно вызвать даже если у вас поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())