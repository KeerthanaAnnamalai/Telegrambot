from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as palm
import sqlite3
import time

TOKEN: Final = 'Your Token'
BOT_USERNAME: Final = '@bananaChoco_bot'
palm.configure(api_key='Your API key')


def create_messages_table(chat_user):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {chat_user} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def send_message(sender, message, chat_user):
    conn = sqlite3.connect('chat.db')
    cursor = conn.cursor()

    cursor.execute(f'INSERT INTO {chat_user} (sender, message) VALUES (?, ?)', (sender, message))
    conn.commit()
    conn.close()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am a Chocolate Bot')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Chocolate, Please type something so I can respond!')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')


def handle_response(text: str) -> str:
    processed: str = text.lower()

    response = palm.chat(messages=processed)

    return response.last


    # if 'hello' in processed:
    #     return 'Hey there!'
    #
    #
    # if 'how are you' in processed:
    #     return 'I am Good!'
    #
    # return 'I do not Understand...'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str=update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}:"{text}"')

    create_messages_table(update.message.chat_id)

    # if message_type == 'group':
    #     if BOT_USERNAME in text:
    #         new_text:str=text.replace(BOT_USERNAME, '').strip()
    #         response:str=handle_response(new_text)
    #     else:
    #         return
    # else:
    response: str=handle_response(text)
    send_message()

    print('BOT:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')


if __name__=='__main__':
    print('Starting bot...')
    app= Application.builder().token(TOKEN).build()


    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))


    app.add_handler(MessageHandler(filters.TEXT,handle_message))

    app.add_error_handler(error)

    print('Polling....')
    app.run_polling(poll_interval=3)






