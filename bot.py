import os
import requests
import yfinance as yf

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    }, timeout=20)

def get_signal():
    data = yf.download(
        "XAUUSD=X",
        period="2d",
        interval="15m",
        progress=False,
        auto_adjust=False
    )

    if data.empty:
        return "⚠️ XAUUSD data unavailable"

    close = data["Close"].squeeze()

    ema9 = close.ewm(span=9, adjust=False).mean().iloc[-1]
    ema21 = close.ewm(span=21, adjust=False).mean().iloc[-1]
    price = close.iloc[-1]

    if ema9 > ema21:
        signal = "🟢 BUY"
    elif ema9 < ema21:
        signal = "🔴 SELL"
    else:
        signal = "⚪ WAIT"

    return (
        "📊 XAUUSD AI SIGNAL\n\n"
        f"💰 Price: {price:.2f}\n"
        f"📈 EMA 9: {ema9:.2f}\n"
        f"📉 EMA 21: {ema21:.2f}\n\n"
        f"🎯 Signal: {signal}\n\n"
        "⏱ Timeframe: 15M\n"
        "⚠️ Signal only — manage risk."
    )

if __name__ == "__main__":
    message = get_signal()
    send_telegram(message)
