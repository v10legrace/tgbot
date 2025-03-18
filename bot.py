import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = "7845096206:AAGY_MDRQ1HjQhgk_4BAkZ9L5Ffnv0xGBFs"
ADMIN_ID = 7005245688  # Твой Telegram user ID
PROFILE_LINK = "https://t.me/tabysmanager"  # Ссылка на твой профиль

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Логирование (чтобы видеть ошибки)
logging.basicConfig(level=logging.INFO)

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Схема"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Чтобы получить схему, нажми на кнопку ниже.", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "Схема")
async def ask_for_video(message: types.Message):
    await message.answer("Чтобы получить схему, нужно пройти верификацию. Отправь мне видео-кружок.")

@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def forward_video(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    await bot.send_message(ADMIN_ID, f"Пользователь @{message.from_user.username} (ID: {user_id}, {user_name}) отправил видео-кружок.\n\nВерифицировать: /verify {user_id}")

@dp.message_handler(commands=['verify'])
async def verify_user(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return  # Игнорируем команду, если её отправил не админ

    try:
        _, user_id = message.text.split()
        user_id = int(user_id)
        await bot.send_message(user_id, f"✅ Ты верифицирован! Вот твоя схема: {PROFILE_LINK}")
        await message.answer(f"Пользователь {user_id} верифицирован!")
    except:
        await message.answer("Ошибка! Используй команду так: /verify user_id")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)