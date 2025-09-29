# bot.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# --- TOKEN ni shu yerga qo'ying ---
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
# ------------------------------------

# Botni yaratishda DefaultBotProperties orqali parse_mode o'rnatamiz
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# /start komandasi
@dp.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👋 Salom deb qaytar", callback_data="say_hi")],
        [InlineKeyboardButton(text="ℹ️ Foydalanuvchi haqida", callback_data="whoami")]
    ])
    await message.answer(
        "<b>Salom!</b>\n\nMen oddiy Telegram botman. Quyidagi tugmalardan birini bosing yoki menga xabar jo'nating — men echo (takrorlash) qilaman.",
        reply_markup=keyboard
    )

# Oddiy echo (foydalanuvchi kiritgan matnni qaytaradi)
@dp.message()
async def echo(message: Message):
    # Botga yuborilgan matnni oddiy qilib qaytaradi
    # Agar stiker, rasm va boshqa turdagi xabar bo'lsa, shunchaki qisqacha javob beradi
    if message.text:
        await message.answer(f"Siz yozdingiz: {message.text}")
    else:
        await message.answer("Men hozir faqat matnli xabarlarni takrorlay olaman :)")

# Inline tugmalar uchun callback handler
@dp.callback_query(Text(equals=["say_hi", "whoami"]))
async def on_button_click(callback: CallbackQuery):
    data = callback.data
    if data == "say_hi":
        await callback.message.answer(f"👋 Salom, {callback.from_user.first_name}!")
    elif data == "whoami":
        u = callback.from_user
        await callback.message.answer(f"👤 Siz: <b>{u.full_name}</b>\nID: <code>{u.id}</code>")
    # callbackni acknowledge qilish (tugma bosilgani ko'rinadi)
    await callback.answer()

# Xatoliklar (opsional): Exceptionlar haqida terminalga chiqarish
async def on_startup():
    print("Bot ishga tushdi...")

async def on_shutdown():
    await bot.session.close()
    print("Bot to'xtatildi, sessiya yopildi.")

# Asosiy funksiyani ishga tushuramiz
async def main():
    try:
        await on_startup()
        # start_polling Dispatcher bilan Bot obyektini uzatamiz
        await dp.start_polling(bot)
    finally:
        await on_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
