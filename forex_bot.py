import yfinance as yf
import pandas_ta as ta
import time
import requests
from datetime import datetime, timedelta

# --- بيانات البوت ---
BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=15)
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")

symbols = ["EURUSD=X", "GBPUSD=X"]

print("البوت يعمل الآن ويحلل البيانات...")

while True:
    for symbol in symbols:
        try:
            # جلب البيانات
            data = yf.download(symbol, period="2d", interval="1m", progress=False)
            
            if not data.empty and len(data) > 15:
                # حساب RSI
                rsi_series = ta.rsi(data['Close'], length=14)
                current_rsi = rsi_series.iloc[-1]
                
                # التحقق الصارم: إذا لم تكن القيمة رقماً، نتخطى هذه الدورة
                if current_rsi is None or str(current_rsi) == 'nan':
                    continue
                
                current_rsi = float(current_rsi)
                
                # تحديد المدة الزمنية تلقائياً (1-5 دقائق)
                if current_rsi < 20 or current_rsi > 80:
                    duration = 5
                elif current_rsi < 25 or current_rsi > 75:
                    duration = 4
                elif current_rsi < 27 or current_rsi > 73:
                    duration = 3
                elif current_rsi < 29 or current_rsi > 71:
                    duration = 2
                else:
                    duration = 1
                
                # وقت الإشارة
                next_minute = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M")
                
                # منطق الإرسال
                if current_rsi < 30:
                    msg = (f"🚀 صفقة قوية (CALL)\nالزوج: {symbol}\nالتوقيت: {next_minute}\nالمدة: {duration} دقيقة\nRSI: {current_rsi:.2f}")
                    send_telegram_msg(msg)
                    time.sleep(2) # تأخير بسيط بين الإشارات
                
                elif current_rsi > 70:
                    msg = (f"🔥 صفقة قوية (PUT)\nالزوج: {symbol}\nالتوقيت: {next_minute}\nالمدة: {duration} دقيقة\nRSI: {current_rsi:.2f}")
                    send_telegram_msg(msg)
                    time.sleep(2)

        except Exception as e:
            print(f"خطأ في {symbol}: {e}")
            
    time.sleep(60) # البوت يفحص كل دقيقة
