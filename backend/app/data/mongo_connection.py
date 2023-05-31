import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.configs.config import Config


MONGO_CONNSTRING = Config.app_settings['mongo']['connection_string']
MONGO_BEVFLIX = Config.app_settings['mongo']['db_name']

client: AsyncIOMotorClient = None

async def get_db_bevflix() -> AsyncIOMotorDatabase:
    return client[MONGO_BEVFLIX]

async def connect_and_init_db():
    global client
    try:
        client = AsyncIOMotorClient(MONGO_CONNSTRING)
        logging.info(f'Connected to {MONGO_BEVFLIX}')
    except Exception as e:
        logging.exception(f'could not connect to mongo {e}')
        raise

async def close_db():
    global client
    if client is None:
        logging.warning('connection is none. nothing to close')
        return
    client.close()
    client = None
    logging.info(f'{MONGO_BEVFLIX} connection closed')



    