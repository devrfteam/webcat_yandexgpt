from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from config import API_TOKEN
from message_handler import start, handle_message

if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN).concurrent_updates(True).build()

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', start)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(message_handler)

    application.run_polling()
