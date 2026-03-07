import logging
import random
import asyncio
from datetime import datetime
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler  # импорт для регестрации обработчика хандлер для лайн кнопок
from data import  questions, questions2, reply_markup, game_markup, viktrina_markup, reply_markup_line
from handlers_text import greet_if_hello
from remimber import reminder, send_reminder
from game_viktrina import  game, viktorina, aktivi_game, aktivi_viktrina
TOKEN = "8420758526:AAHbHgvanf3pwtASdRA5MI4zkWw_RjtguHE"
GAME = False
VIKTORINA = False
VOPROS_INDEX = 0
ATTEMPS = 0
SIGRAN_RAUND = 0  # раунды
MAX_GAMES = 5  # макс раундов
POBEDA_BOT = 0  # победа бота
POBEDA_IGROK = 0  # победа игрока

logging.basicConfig(level=logging.INFO)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! Я твой бот. Чем могу помочь?",
        reply_markup=reply_markup
    )
    await update.message.reply_text(
        "давай знакомиться",
        reply_markup=reply_markup_line
    )

async def line_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    text = query.data
    await query.answer()

    if text == "name":
        await query.edit_message_text(text="как тебя зовут?",
                                      reply_markup=None
                                      )
        # сохраняем состояние и ждем ввода пользоваеля
        context.user_data['ozhidanie_otveta'] = 'name'


    elif text == "age":
        await query.edit_message_text(text="сколько тебе лет?",
                                      reply_markup=None
                                      )
        context.user_data['ozhidanie_otveta'] = 'age'

    elif text == "address":
        await query.edit_message_text(text="где ты живешь?",
                                      reply_markup=None
                                      )
        context.user_data['ozhidanie_otveta'] = 'address'

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("game", game))
app.add_handler(CommandHandler("viktorina", viktorina))
app.add_handler(CommandHandler("reminder", reminder))
app.add_handler(CallbackQueryHandler(line_button))  # этот обработчик обрабатывает именно нажатие лайн кнопок, поблема в том что срабатывает ее дефолтный ответ
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greet_if_hello))
app.run_polling()