from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dex_checker import analyze_token
import os

API_TOKEN = os.getenv("BOT_TOKEN")
if not API_TOKEN:
    print("❌ BOT_TOKEN environment variable bai samuwa ba.")
    exit()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.add(KeyboardButton("🛠 Yadda Bot ɗin Ke Aiki"))

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("👋 Barka da zuwa DEX Token Checker Bot.
Zaɓi daga menu:", reply_markup=menu_kb)

@dp.message_handler(lambda msg: msg.text == "🛠 Yadda Bot ɗin Ke Aiki")
async def how_it_works(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("⬅️ Komawa Menu"))
    await message.answer(
        "✍️ Don duba wani token, yi amfani da umurnin:

/check_all <contract_address>

"
        "📌 Misali:
/check_all 0xe9e7cea3dedca5984780bafc599bd69add087d56",
        reply_markup=kb
    )

@dp.message_handler(lambda msg: msg.text == "⬅️ Komawa Menu")
async def back_to_menu(message: types.Message):
    await start_handler(message)

@dp.message_handler(commands=["check_all"])
async def check_all_handler(message: types.Message):
    parts = message.text.split()
    if len(parts) != 2:
        await message.reply("⚠️ Da fatan za a saka contract address: /check_all <address>")
        return

    address = parts[1]
    status = await analyze_token(address)
    await message.reply(status)

if __name__ == "__main__":
    executor.start_polling(dp)