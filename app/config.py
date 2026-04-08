import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI :str= os.getenv("MONGODB_URI")
    DB_NAME = 'mainDB'

settings = Settings()