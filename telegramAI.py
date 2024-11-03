TELEGRAM_BOT_NAME = '@netherman_bot'

import os
from dotenv import load_dotenv
from telegram import MenuButtonWebApp, Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import ChatBot

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
   context.chat_data["chatHistory"] = []
   await update.message.reply_text("Hello I'm a netherman_bot powered by AI. How can I help you?")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    chat_id = update.effective_chat.id
    
    if "chatHistory" not in context.chat_data:
        context.chat_data["chatHistory"] = []
    
    context.chat_data["chatHistory"].append({
        "role": "user",
        "content": message_text,
        "message_id": update.message.message_id
    })
    
    chat_history = context.chat_data["chatHistory"]

    chatBot = ChatBot.ChatBot()
    response = await chatBot.askAI(message_text, chat_history)

    context.chat_data["chatHistory"].append({
        "role": "assistant",
        "message_id": update.message.message_id,
        "content": response
    })

    chat_history = context.chat_data["chatHistory"]

    print('chat history:')
    for message in chat_history:
        print(message['role'] + ": " + message['content'])

    await update.message.reply_text(response)

async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f" error")

if __name__ == "__main__":

    load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    print('start bot...')
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler (CommandHandler('start', start_command))

    app.add_handler(CommandHandler('new', start_command))

    app.add_error_handler(handle_error)

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("polling")
    app.run_polling(poll_interval=5)
