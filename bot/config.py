from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    API_KEY = os.getenv("API_KEY")
    BOT_TOKEN = os.getenv("BOT_TOKEN")


settings = Settings()
