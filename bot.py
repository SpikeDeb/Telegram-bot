import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "8691147645:AAEzGq3XMQwu_QRr38z-gYzOCwKEkMrib-s"
PAYMENT_LINK = "https://pages.razorpay.com/pl_TXat4m9nT97OpF"
SERVICE_ACCESS_LINK = "https://t.me/+2fSZq6QcsdJiOGY1"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛒 Buy Now", url=PAYMENT_LINK)],
            [InlineKeyboardButton(text="✅ Check Payment", callback_data="check_payment")]
        ]
    )
    
    caption_text = (
        "🔥 <b>BIGGEST VIRAL VIDEO BUNDLE</b> 🔥\n\n"
        "🔞 <b>VVIP MEGA COLLECTION 2026</b> 🔞\n"
        "───────────────────\n"
        "✨ <b>ALL PREMIUM CATEGORIES:</b>\n\n"
        "<b>50,000+ Desi Hindi Videos</b> 🥵\n\n"
        "🔸 MOM-SON\n"
        "🔸 DESI BHABHI\n"
        "🔸 INSTAGR@M LEAKS\n"
        "🔸 BR@THER-SISTER\n"
        "🔸 AUNTY-P*RN\n"
        "🔸 COLLEGE ROM@NCE\n"
        "🔸 Aunty & Housewife\n\n"
        "<b>Lifetime Access / Free Update</b>\n\n"
        "💎 <b>FULL ACCESS ONLY AT: ₹295/-</b> ✅"
    )
    
    banner_url = "https://picsum.photos/800/500"
    await message.answer_photo(photo=banner_url, caption=caption_text, reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query(F.data == "check_payment")
async def verify_payment(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Access Service Now", url=SERVICE_ACCESS_LINK)]
        ]
    )
    await callback.message.answer(
        text="🎉 <b>Payment verified successfully!</b>\n\nNiche diye gaye button se service access karein:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

async def main():
    print("Bot start ho gaya hai...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
