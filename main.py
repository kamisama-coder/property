import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

# now we have them as a handy python strings!
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('Bot_USERNAME')


async def launch_web_ui1(update: Update, callback: CallbackContext):
    # For now, let's just acknowledge that we received the command
    await update.effective_chat.send_message("I hear you loud and clear !")
 
async def launch_web_ui2(update: Update, callback: CallbackContext):
    # For now, we just display google.com...
    kb = [
        [KeyboardButton("Show me Google!", web_app=WebAppInfo("http://127.0.0.1:5000"))]
    ]
    dict = {}
    dict['id' ]= update.message.from_user.id
    dict['username'] = update.message.from_user.username
    await update.message.reply_text(f"it's your user_ID {dict['id']}", reply_markup=ReplyKeyboardMarkup(kb))

async def launch_web_ui2(update: Update, callback: CallbackContext):
    # For now, we just display google.com...
    kb = [
        [KeyboardButton("Show me Google!", web_app=WebAppInfo("http://127.0.0.1:5000/proficency"))]
    ]
    await update.message.reply_text(f"it's your user_ID {dict['id']}", reply_markup=ReplyKeyboardMarkup(kb))    

async def launch_web_ui3(update: Update, callback: CallbackContext):
    # For now, we just display google.com...
    new = update.message.from_user.id
    kb = [
        [KeyboardButton("Show me Google!", web_app=WebAppInfo("http://127.0.0.1:5000/admin/" + new))]
    ]
    await update.message.reply_text(f"it's your user_ID {dict['id']}", reply_markup=ReplyKeyboardMarkup(kb))


if __name__ == '__main__':
    # when we run the script we want to first create the bot from the token:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # and let's set a command listener for /start to trigger our Web UI
    application.add_handler(CommandHandler('registration', launch_web_ui1))
    application.add_handler(CommandHandler('search', launch_web_ui2))
    application.add_handler(CommandHandler('admin', launch_web_ui3))
    

    # and send the bot on its way!
    print(f"Your bot is listening! Navigate to http://t.me/{BOT_USERNAME} to interact with it!")
    application.run_polling()