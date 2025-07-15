import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('Bot_USERNAME')


async def launch_web_ui1(update: Update, callback: CallbackContext):

    dict = {}
    dict['id' ]= update.message.from_user.id
    dict['username'] = update.message.from_user.username
    kb = [
        [KeyboardButton("Show me Google!", web_app=WebAppInfo("https://property-1-qqtg.onrender.com/" + str(dict['id'])))]
    ]
    await update.effective_chat.send_message("I hear you loud and clear !",reply_markup=ReplyKeyboardMarkup(kb))
 
async def launch_web_ui28(update: Update, callback: CallbackContext):

    dict = {}
    dict['id' ]= update.message.from_user.id
    dict['username'] = update.message.from_user.username
    await update.message.reply_text(f"it's your user_ID {dict['id']}\n and your username is {dict['username']}")

async def launch_web_ui2(update: Update, callback: CallbackContext):

    kb = [
        [KeyboardButton("Show me Google!", web_app=WebAppInfo("https://property-1-qqtg.onrender.com/proficency"))]
    ]
    await update.message.reply_text(f"it's your user_ID {dict['id']}", reply_markup=ReplyKeyboardMarkup(kb))    

async def launch_web_ui3(update: Update, callback: CallbackContext):
    
    new = update.message.from_user.id
    kb = [
        [KeyboardButton("Show me Google!", web_app=WebAppInfo("https://property-1-qqtg.onrender.com/admin/" + str(new)))]
    ]
    await update.message.reply_text(f"it's your user_ID {dict['id']}", reply_markup=ReplyKeyboardMarkup(kb))


if __name__ == '__main__':

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('registration', launch_web_ui1))
    application.add_handler(CommandHandler('search', launch_web_ui2))
    application.add_handler(CommandHandler('admin', launch_web_ui3))
    application.add_handler(CommandHandler('imformation', launch_web_ui28))
    

    print(f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()