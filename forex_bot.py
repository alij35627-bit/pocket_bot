import telebot
import os
from flask import Flask, request

app = Flask(__name__)
API_KEY = os.environ.get('API_KEY')
CHAT_ID = os.environ.get('CHAT_ID') # سنضيف هذا لاحقاً ليعرف البوت لمن يرسل
bot = telebot.TeleBot(API_KEY)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        message = data.get('message')
        bot.send_message(CHAT_ID, message)
        return "Message sent", 200
    return "No data", 400

if __name__ == '__main__':
    # تشغيل Flask لاستقبال الإشارات
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

bot.polling(none_stop=True)

bot.polling(none_stop=True)
