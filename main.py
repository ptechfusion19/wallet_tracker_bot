import asyncio
import logging
import sys
from support_utils.imports import bot , dp
from aiogram.enums import ParseMode
from handlers.Call_back import router

from aiogram.utils.markdown import hbold






async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())