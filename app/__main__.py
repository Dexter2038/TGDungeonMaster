import asyncio
from os import environ
from aiogram import Bot, Dispatcher

import dotenv
from app.handlers.main import router


dotenv.load_dotenv(dotenv_path=".env")

try:
    bot = Bot(token=environ['BOT_TOKEN'])
    dp = Dispatcher()
except KeyError:
    raise RuntimeError('BOT_TOKEN is not set')
except Exception as e:
    raise e


dp.include_router(router)
asyncio.get_event_loop().run_until_complete(dp.start_polling(bot))
