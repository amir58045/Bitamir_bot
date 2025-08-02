from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

ADMIN_CHAT_ID = 7316295445
ORDERS_FILE = "orders.txt"

custom_keyboard = [
    ["📂 دریافت نسخه تستی", "💳 خرید"],
    ["🆘 پشتیبانی", "📝 ثبت سفارش"]
]
reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لطفا یکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📂 دریافت نسخه تستی":
        try:
            await update.message.reply_document(document=open("demo_expert.ex5", "rb"))
        except Exception as e:
            await update.message.reply_text(f"خطا در ارسال فایل: {e}")

    elif text == "💳 خرید":
        await update.message.reply_text(
            "💳 (یا معادل تومان)\n"
            "برای پرداخت از آدرس‌های زیر استفاده کنید. سفارش در کمتر از ۱۵ دقیقه تکمیل خواهد شد:\n"
            "BEP20:\n`0x1627Cf122aC0EA8880144D8D65bBD927ee1594dD`\n"
            "TRC20:\n`TMkHUjTQA1u4qBE84G4QdZKPkNgEZo1a1e`\n"
            "پس از پرداخت، برای دریافت فایل خریداری‌شده با دکمه «📝 ثبت سفارش» اقدام کن.",
            parse_mode="Markdown"
        )

    elif text == "🆘 پشتیبانی":
        await update.message.reply_text("🆘 برای پشتیبانی با این آی‌دی تماس بگیر:\n@hossein_sfrr")

    elif text == "📝 ثبت سفارش":
        await update.message.reply_text("لطفا شماره فیش پرداخت یا اطلاعات سفارش خود را ارسال کنید:")
        context.user_data["waiting_order"] = True

    else:
        if context.user_data.get("waiting_order"):
            user = update.message.from_user
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order_line = f"{now} | User ID: {user.id} | Username: @{user.username} | Info: {text}\n"

            with open(ORDERS_FILE, "a", encoding="utf-8") as f:
                f.write(order_line)

            await update.message.reply_text("✅ سفارش شما ثبت شد. پس از بررسی، فایل برای شما ارسال خواهد شد.")
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"سفارش جدید:\n{order_line}")

            context.user_data["waiting_order"] = False
        else:
            await update.message.reply_text("لطفا یکی از دکمه‌ها را انتخاب کنید.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
