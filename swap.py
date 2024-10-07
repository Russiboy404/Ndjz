

import requests
import json
import telebot
from telebot import types

TOKEN = "7100323131:AAEMkGNHtafRL4IqmCjDsr6-RwRuCWMwK6Y"
bot = telebot.TeleBot(TOKEN)
url = "https://rayan-api.rayyan-ex.com:44896/api/services/app/ExchangeCurrency/ConvertCurrency"

# Updated dictionary with more currencies and their IDs
currency_ids = {
    "USD": 6,   # US Dollar
    "EUR": 7,   # Euro
    "GBP": 8,   # British Pound
    "SAR": 9,   # Saudi Riyal
    "AED": 10,  # United Arab Emirates Dirham
    "AUD": 11,  # Australian Dollar
    "JOD": 12,  # Jordanian Dinar
    "KWD": 13,  # Kuwaiti Dinar
    "BHD": 14,  # Bahraini Dinar
    "QAR": 15,  # Qatari Riyal
    "OMR": 16,  # Omani Rial
    "CAD": 17   # Canadian Dollar
}

# Function to generate inline buttons with currency options and flags
def currency_inline_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("🇺🇸 USD", callback_data="USD"),
        types.InlineKeyboardButton("🇪🇺 EUR", callback_data="EUR"),
        types.InlineKeyboardButton("🇬🇧 GBP", callback_data="GBP"),
        types.InlineKeyboardButton("🇸🇦 SAR", callback_data="SAR"),
        types.InlineKeyboardButton("🇦🇪 AED", callback_data="AED"),
        types.InlineKeyboardButton("🇦🇺 AUD", callback_data="AUD"),
        types.InlineKeyboardButton("🇯🇴 JOD", callback_data="JOD"),
        types.InlineKeyboardButton("🇰🇼 KWD", callback_data="KWD"),
        types.InlineKeyboardButton("🇧🇭 BHD", callback_data="BHD"),
        types.InlineKeyboardButton("🇶🇦 QAR", callback_data="QAR"),
        types.InlineKeyboardButton("🇴🇲 OMR", callback_data="OMR"),
        types.InlineKeyboardButton("🇨🇦 CAD", callback_data="CAD")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, '''
🇺🇸 Dollar To Dinar 🇮🇶
سڵاو من بۆتێکم دەتوانم نرخی دۆلار بەرامبەر دینار ئاڵو گۆڕ بکەم بە نرخی ئێستا
ئێستا ئەو دراوە هەڵبژێرە کە دەتەوێت بیگۆڕم بۆسەر دیناری عێراقی
   Founder @Ak4aa ''', reply_markup=currency_inline_keyboard())

# This handler processes the button clicks
@bot.callback_query_handler(func=lambda call: call.data in currency_ids.keys())
def ask_amount(call):
    currency = call.data
    bot.send_message(call.message.chat.id, f"ئێستا بڕی ئەو دراوە بنێرە کە دەتەوێت {currency}")
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, lambda msg: convert_currency(msg, currency))

def convert_currency(message, currency):
    try:
        amount = float(message.text)
        currency_id = currency_ids[currency]

        payload = json.dumps({
            "id": currency_id,
            "amount": str(amount),
            "isReverse": False
        })

        headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36",
            'Accept': "application/json, text/plain, */*",
            'Content-Type': "application/json",
            'origin': "https://www.rayyan-ex.iq"
        }

        response = requests.post(url, data=payload, headers=headers)
        response_data = response.json()

        if 'result' in response_data:
            amountPerCurrency = response_data['result']['amountPerCurrency']
            totalAmount = response_data['result']['totalAmount']
            formatted_number = "{:,}".format(totalAmount)
            bot.reply_to(message, f'''
بەهای گۆڕینەوە بریتیە لە {formatted_number} دیناری عێراقی
بڕی یەک\n {currency}\n {amountPerCurrency} دیناری عێراقی
          Founder @Ak4aa   ''', reply_markup=currency_inline_keyboard()) # Resend the currency selection buttons
        else:
            bot.reply_to(message, "There was an error in processing your request", reply_markup=currency_inline_keyboard())

    except ValueError:
        bot.reply_to(message, "Please enter a valid amount", reply_markup=currency_inline_keyboard())

bot.polling()
