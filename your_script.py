# -*- coding: utf-8 -*-
"""Untitled14.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1v0ePe5m1VL3GhKuP0NUxzMxh8mIIdKqr
"""

# pip install python-telegram-bot

import requests

# Your Bot Token from BotFather
TOKEN = '7734827684:AAHZHGg5_10KO00HZ6KJsEM0aarxQLvGMLM'

# Your Chat ID
CHAT_ID = '1134215379'

# Function to send a message
def send_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.text}")

# Example usage
message = "-- -- -- -- -- -- -- -- -- -- --"
send_message(TOKEN, CHAT_ID, message)


# -------------------------------------------------------
# -------------------------------------------------------
# -------------------------------------------------------

import requests
import yfinance as yf
from datetime import datetime, timedelta

# Telegram Bot Notification Function
def send_telegram_notification(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"Notification sent: {message}")
    else:
        print(f"Failed to send notification: {response.text}")

# Function to fetch strict period-based history
def fetch_strict_history(stock_symbol):
    today = datetime.today().date()
    weekday = today.weekday()

    # Calendar-based date ranges
    start_daily = today
    end_daily = today + timedelta(days=1)

    start_week = today - timedelta(days=weekday)
    end_week = today + timedelta(days=1)

    start_month = today.replace(day=1)
    end_month = today + timedelta(days=1)

    stock = yf.Ticker(stock_symbol.upper() + ".NS")

    return {
        'DAILY': (stock.history(start=start_daily, end=end_daily), start_daily),
        'WEEKLY': (stock.history(start=start_week, end=end_week), start_week),
        'MONTHLY': (stock.history(start=start_month, end=end_month), start_month)
    }

# Breakout detection logic
def calculate_breakout(hist, current_price):
    resistance = hist['Close'].max()
    support = hist['Close'].min()
    breakout_type = None
    if current_price >= resistance:
        breakout_type = "Upward Breakout"
    elif current_price <= support:
        breakout_type = "Downward Breakout"
    return resistance, support, breakout_type

# Main logic
def monitor_stocks(stock_symbols, token, chat_id):
    for stock_symbol in stock_symbols:
        print(f"Checking {stock_symbol}...")
        all_data = fetch_strict_history(stock_symbol)
        breakout_messages = []

        for label in ['DAILY', 'WEEKLY', 'MONTHLY']:
            hist, _ = all_data[label]
            if hist.empty:
                breakout_messages.append(f"NO {label} BREAKOUT")
                continue
            current_price = hist['Close'].iloc[-1]
            resistance, support, breakout_type = calculate_breakout(hist, current_price)
            if breakout_type:
                msg = (f"----- ----- {label} BREAKOUT ----- -----\n"
                       f"curr price: {current_price:.2f}\n"
                       f"res: {resistance:.2f}\n"
                       f"sup: {support:.2f}\n"
                       f"type: {breakout_type}\n"
                       f"----- ----- ----- ----- ----- ----- -----")
                breakout_messages.append(msg)
            else:
                breakout_messages.append(f"NO {label} BREAKOUT")

        final_message = f"Breakout Alert for {stock_symbol}!\n\n" + "\n\n".join(breakout_messages)
        send_telegram_notification(token, chat_id, final_message)

# Telegram Bot Credentials
TOKEN = '7734827684:AAHZHGg5_10KO00HZ6KJsEM0aarxQLvGMLM'
CHAT_ID = '1134215379'

# Stocks to Monitor
STOCKS = [
    'TCS', 'RELIANCE', 'TATAPOWER', 'IDEA', 'YESBANK', 'IRFC', 'ZOMATO', 'SUZLON',
    'TATASTEEL', 'MSTCLTD', 'TATAMOTORS', 'ONGC', 'PNB', 'LAURUSLABS', 'UPL', 'LTF',
    'INFY', 'WIPRO', 'BAJAJFINSV', 'CIPLA', 'JSWSTEEL', 'HDFCBANK', 'TATACHEM', 'BPCL',
    'SUNPHARMA', 'COROMANDEL', 'IGL', 'ICICIBANK', 'LT', 'M&M', 'OBEROIRLTY', 'SBIN',
    'TATACONSUM', 'TVSMOTOR', 'PVRINOX', 'APOLLOHOSP', 'ASHOKLEY', 'AMBUJACEM', 'CONCOR',
    'BIOCON'
]

# One-time check (triggered manually)
monitor_stocks(STOCKS, TOKEN, CHAT_ID)

