from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Загрузите переменные среды из файла .env

class Settings(BaseSettings):
    bot_token: str
    pay_token: str

# Создайте экземпляр класса Settings
settings = Settings()

# Теперь вы можете использовать переменные
# print(settings.database_url)
# print(settings.api_key)
