from aiogram import executor
from bot.config import dp, bot
from bot import handlers

async def on_startup(_):
    print("Attempting to get bot info...")  # Отладка
    try:
        me = await bot.get_me()
        print(f"Bot is running as {me.username}")
    except Exception as e:
        print(f"Failed to get bot info: {e}")


if __name__ == "__main__":
    print("Starting bot...")  # Отладка
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
