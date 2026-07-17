import telebot
import time
import os

# قراءة التوكن من متغيرات البيئة في Railway
API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)

def analyze_market(prices):
    trend = prices[-1] - prices[0]
    if trend > 0:
        return "🟢 إشارة شراء (CALL UP) - اتجاه صاعد قوي", "UP"
    elif trend < 0:
        return "🔴 إشارة بيع (PUT DOWN) - اتجاه هابط قوي", "DOWN"
    else:
        return "⚠️ السوق متذبذب، لا تدخل", None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "البوت يعمل! أرسل لي أسعار الإغلاق لآخر 5 شموع مفصولة بمسافة")

@bot.message_handler(func=lambda message: True)
def handle_prices(message):
    try:
        prices = [float(x) for x in message.text.split()]
        if len(prices) != 5:
            bot.reply_to(message, "يرجى إرسال 5 أسعار فقط!")
            return
        result, direction = analyze_market(prices)
        if direction:
            res = (f"📊 CAD/CHF-OTC\n⏰ {time.strftime('%I:%M %p')}\n⌛️ 1 Minutes\n{'🟢 CALL UP ⬆️' if direction == 'UP' else '🔴 PUT DOWN ⬇️'}")
            bot.reply_to(message, res)
        else:
            bot.reply_to(message, result)
    except ValueError:
        bot.reply_to(message, "خطأ في البيانات. تأكد من إرسال أرقام فقط.")

bot.polling(none_stop=True)

bot.polling(none_stop=True)
