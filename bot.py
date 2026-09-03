import os
import logging
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import uvicorn

# Aapka Bot Token, Razorpay Payment Link, aur Channel Link
BOT_TOKEN = "8907533487:AAFcPAxB7hqiyf5MNfyK9PbTGkX1n0lv30g"
PAYMENT_LINK = "https://pages.razorpay.com/pl_TXat4m9nT97OpF"
SERVICE_ACCESS_LINK = "https://t.me/+2fSZq6QcsdJiOGY1"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

user_sessions = {}

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    user_sessions[message.from_user.id] = message.chat.id
    
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
    await callback.answer(
        text="⏳ Payment abhi confirm nahi hui hai. Payment hone ke baad automatic link mil jayega!",
        show_alert=True
    )

@app.post("/webhook/razorpay")
async def razorpay_webhook(request: Request):
    data = await request.json()
    
    if data.get("event") == "payment.link.paid" or data.get("event") == "payment.captured":
        for user_id, chat_id in user_sessions.items():
            success_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🚀 Access Service Now", url=SERVICE_ACCESS_LINK)]
                ]
            )
            text = (
                "🎉 <b>Payment Successful!</b>\n\n"
                "Aapka payment automatically verify ho gaya hai. Niche diye gaye button se service access karein:"
            )
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=success_keyboard, parse_mode="HTML")
            
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(dp.start_polling(bot))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
