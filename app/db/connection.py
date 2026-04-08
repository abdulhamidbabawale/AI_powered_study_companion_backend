# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# from app.config import Settings

# # Create a new client and connect to the server
# client = MongoClient(Settings.MONGODB_URI, server_api=ServerApi('1'))
# db = client[Settings.DB_NAME] 
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


client = AsyncIOMotorClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]
