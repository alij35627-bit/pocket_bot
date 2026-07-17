import telebot
from telebot import types
import yfinance as yf
import time
import threading
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "Gemini Jaafar Pro Max is Active!"

BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"

# تفعيل البوت
bot = telebot.TeleBot(BOT_TOKEN)

# إعداد القائمة
bot.set_my_commands([
    types.BotCommand("start", "تشغيل"), 
    types.BotCommand("report", "عرض التقرير"),
    types.BotCommand("status", "حالة البوت")
])
stats = {"win": 0, "loss": 0, "skipped": 0}

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "win": stats["win"] += 1
    elif call.data == "loss": stats["loss"] += 1
    elif call.data == "skipped": stats["skipped"] += 1
    bot.answer_callback_query(call.id, f"تم تسجيل: {call.data}")

@bot.message_handler(commands=['report'])
def get_report(message):
    total = stats["win"] + stats["loss"]
    win_rate = (stats["win"] / total * 100) if total > 0 else 0
    bot.reply_to(message, f"📊 التقرير:\nالربح: {stats['win']}\nالخسارة: {stats['loss']}\nلم أدخل: {stats['skipped']}\nنسبة النجاح: {win_rate:.2f}%")

@bot.message_handler(commands=['status'])
def get_status(message):
    bot.reply_to(message, "🤖 جعفر برو ماكس يعمل الآن ويراقب الأسواق.. صبراً على الفرصة الذهبية!")

def run_bot():
    while True:
        # هنا سيتم إضافة منطق التداول الخاص بك لاحقاً
        time.sleep(60)

if __name__ == "__main__":
    # تنظيف الاتصالات القديمة
    bot.remove_webhook()
    
    # 1. تشغيل خيط التداول
    threading.Thread(target=run_bot, daemon=True).start()
    
    # 2. تشغيل خيط البوت
    threading.Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5), daemon=True).start()
    
    # 3. تشغيل سيرفر Flask
    app.run(host='0.0.0.0', port=8080)
