import telebot
from telebot import types
import os
import requests
import json

url = 'https://us-central1-chat-for-chatgpt.cloudfunctions.net/basicUserRequestBeta'

def gpt(text) -> str:
 headers = {
     'Host': 'us-central1-chat-for-chatgpt.cloudfunctions.net',
     'Connection': 'keep-alive',
     'If-None-Match': 'W/"1c3-Up2QpuBs2+QUjJl/C9nteIBUa00"',
     'Accept': '*/*',
     'User-Agent': 'com.tappz.aichat/1.2.2 iPhone/15.6.1 hw/iPhone8_2',
     'Content-Type': 'application/json',
     'Accept-Language': 'en-GB,en;q=0.9'
 }

 data = {
     'data': {
         'message':text,
     }
 }

 response = requests.post(url, headers=headers, data=json.dumps(data))
 try:
  result = response.json()["result"]["choices"][0]["text"]
  return result
 except:
  return None

idch = os.environ.get("idch")
userid = os.environ.get("id")

bot = telebot.TeleBot(os.environ.get("token"))
CHANNEL_ID = idch


def check_subscription(user_id):
    user = bot.get_chat_member(CHANNEL_ID, user_id)
    if user.status == "member" or user.status == "creator" or user.status == "administrator":
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username
    user_language_code = message.from_user.language_code
    user_info = f"New user:\nFirst name: {user_first_name}\nLast name: {user_last_name}\nUsername: @{user_username}\nUser ID: {user_id}\nLanguage code: {user_language_code}"
    bot.send_message(userid, user_info)
    if check_subscription(user_id):
        bot.send_message(message.chat.id, "مرحبًا بك في البوت! ارسل لي مشكلتك او ماذا تريد مني وسانفذ لك كل شيء")
    else:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="الاشتراك في القناة", url="https://t.me/UI_XB")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "يجب عليك الاشتراك في القناة لاستخدام هذا البوت.", reply_markup=keyboard) 


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = gpt(message.text)
    user_id = message.from_user.id
    if check_subscription(user_id):
      bot.send_message(message.chat.id, text)
    else:
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="الاشتراك في القناة", url="https://t.me/bsjeijxs")
        keyboard.add(url_button)
        bot.send_message(message.chat.id, "يجب عليك الاشتراك في القناة لاستخدام هذا البوت.", reply_markup=keyboard) 

    

bot.infinity_polling()
print("تم شتغل")
