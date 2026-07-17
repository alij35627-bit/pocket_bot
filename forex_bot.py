import yfinance as yf
import pandas_ta as ta
import time
import requests

# --- تم دمج بياناتك ---
BOT_TOKEN = "8821873307:AAF6_suA6IibkRFpui3Bhfh7DwtZLR0VbbI"
CHAT_ID = "8475991182"
# ----------------------

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=10)
    except Exception as e:
        print(f"خطأ في إرسال التنبيه: {e}")

symbols = ["EURUSD=X", "GBPUSD=X"]

print("البوت يعمل الآن ويراقب السوق...")

while True:
    for symbol in symbols:
        try:
            # جلب بيانات الزوج
            data = yf.download(symbol, period="1d", interval="1m", progress=False)
            
            if not data.empty:
                # حساب RSI
                data['RSI'] = ta.rsi(data['Close'], length=14)
                current_rsi = data['RSI'].iloc[-1]
                
                # التحقق من الشروط
                if current_rsi < 30:
                    send_telegram_msg(f"🚀 فرصة شراء (CALL) على {symbol}\nRSI الحالي: {current_rsi:.2f}")
                elif current_rsi > 70:
                    send_telegram_msg(f"🔥 فرصة بيع (PUT) على {symbol}\nRSI الحالي: {current_rsi:.2f}")
        
        except Exception as e:
            print(f"خطأ في فحص {symbol}: {e}")
            
    # انتظار دقيقة للفحص التالي
    time.sleep(60)
