import telebot
from telebot import types
import yfinance as yf
import pandas_ta as ta
import time
from datetime import datetime, timedelta
import threading

# إعداد البوت
BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"
bot = telebot.TeleBot(BOT_TOKEN)

# إضافة قائمة الأوامر التلقائية
bot.set_my_commands([
    types.BotCommand("start", "تشغيل البوت"),
    types.BotCommand("report", "عرض تقرير الأداء اليومي")
])

# تخزين الإحصائيات
stats = {"win": 0, "loss": 0, "skipped": 0}

# دالة إرسال الإشارة مع أزرار التفاعل
def send_signal(msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ ربح", callback_data="win"),
        types.InlineKeyboardButton("❌ خسارة", callback_data="loss"),
        types.InlineKeyboardButton("🚫 لم أدخل", callback_data="skipped")
    )
    bot.send_message(CHAT_ID, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "win": stats["win"] += 1
    elif call.data == "loss": stats["loss"] += 1
    elif call.data == "skipped": stats["skipped"] += 1
    bot.answer_callback_query(call.id, f"تم تسجيل: {call.data} ✅")

# أمر عرض التقرير
@bot.message_handler(commands=['report'])
def get_report(message):
    total = stats["win"] + stats["loss"]
    win_rate = (stats["win"] / total * 100) if total > 0 else 0
    bot.reply_to(message, f"📊 **تقرير جعفر الاحترافي**:\n\nالربح: {stats['win']} ✅\nالخسارة: {stats['loss']} ❌\nلم أدخل: {stats['skipped']} 🚫\nنسبة النجاح: {win_rate:.2f}%")

# ... (باقي كود التحليل والتشغيل كما هو) ...

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    bot.polling(none_stop=True)
