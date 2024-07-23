import logging
import os
import tempfile
import time
import traceback
from telegram import Update
from telegram.ext import ContextTypes
from aiohttp import ClientSession
from content_handler import fetch_content, extract_text, classify_text
import json

logging.basicConfig(level=logging.WARNING)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне URL, и я отправлю тебе категорию контента сайта.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if 'http' not in update.message.text:
        await update.message.reply_text(f"Укажите полный URL с протоколом http/https")
        return

    try:
        start_time = time.time()
        html = await fetch_content(url)
        text = await extract_text(html)
        result = await classify_text(text)
        
        if 'error' in result:
            await update.message.reply_text(result['error'])
        else:
            category = result['result']['alternatives'][0]['message']['text']
            full_output = json.dumps(result, ensure_ascii=False, indent=2)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                temp_file.write(full_output.encode('utf-8'))
                temp_file_path = temp_file.name

            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_text_file:
                temp_text_file.write(text.encode('utf-8'))
                temp_text_file_path = temp_text_file.name

            end_time = time.time()
            execution_time = end_time - start_time
            
            await update.message.reply_document(document=open(temp_file_path, 'rb'), filename=os.path.basename(temp_file_path))
            await update.message.reply_document(document=open(temp_text_file_path, 'rb'), filename=os.path.basename(temp_text_file_path))
            await update.message.reply_text(f"Категория контента: {category}")
            await update.message.reply_text(f"Время категоризации: {execution_time:.2f} секунд")
        
    except Exception as e:
        logging.error("Произошла ошибка: %s", traceback.format_exc())
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")
