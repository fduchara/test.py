import random
import asyncio
from datetime import datetime
from telegram.ext import ContextTypes
from telegram import Update
from data import questions2, reply_markup, game_markup, viktrina_markup, reply_markup_line
from game_viktrina import game, viktorina, aktivi_game, aktivi_viktrina
from remimber import send_reminder

GAME = False
VIKTORINA = False
VOPROS_INDEX = 0
ATTEMPS = 0
SIGRAN_RAUND = 0
MAX_GAMES = 5
POBEDA_BOT = 0
POBEDA_IGROK = 0
napminani = {}

async def greet_if_hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global GAME, VIKTORINA, VOPROS_INDEX, ATTEMPS, SIGRAN_RAUND, MAX_GAMES, POBEDA_BOT, POBEDA_IGROK
    text = update.message.text.lower()
    dannie = context.user_data.get('ozhidanie_otveta')
    reply = 'Я пока не умею отвечать на такое(.'

    if dannie:
        if dannie == 'name':
            context.user_data['ozhidanie_otveta'] = None
            await update.message.reply_text(
                f"Приятно познакомиться, {text}! А я просто бот и у меня пока нет имени"
            )
            await update.message.reply_text("Продолжим знакомство", reply_markup=reply_markup_line)
            return
        elif dannie == 'age':
            context.user_data['ozhidanie_otveta'] = None
            await update.message.reply_text(f"Понял, тебе {text}", reply_markup=reply_markup_line)
            return
        elif dannie == 'address':
            context.user_data['ozhidanie_otveta'] = None
            await update.message.reply_text(f"{text} — хороший город.", reply_markup=None)
            return

    if text == "стоп":
        GAME = False
        VIKTORINA = False
        await update.message.reply_text(
            "Программа остановлена. Пока!",
            reply_markup=reply_markup
        )
        return

    if GAME:
        response = aktivi_game(text)
        await update.message.reply_text(response, reply_markup=game_markup)
        return

    if VIKTORINA:
        response = aktivi_viktrina(text, context)
        await update.message.reply_text(response, reply_markup=viktrina_markup)
        return

    if context.user_data.get('waiting_for_reminder'):
        user_input = update.message.text
        parts = user_input.split(maxsplit=2)

        if len(parts) != 3:
            await update.message.reply_text(
                "Ошибка: введите дату, время и текст напоминания в формате: ГГ.ММ.ДД ЧЧ:ММ:СС Текст напоминания"
            )
            return
        date_user, time_user, reminder_text = parts

        try:
            # разбираем дату
            date_parts = list(map(int, date_user.split('.')))
            if len(date_parts) != 3:
                raise ValueError("Неверный формат даты. Ожидаемый формат: ГГ.ММ.ДД")
            year = year = 2000 + date_parts[0]   # год
            month = date_parts[1]  # месяц
            day = date_parts[2]    # день

            # разбираем время
            time_parts = list(map(int, time_user.split(':')))
            if len(time_parts) != 3:
                raise ValueError("Неверный формат времени")
            hour = time_parts[0]    # часы
            minute = time_parts[1]  # минуты
            second = time_parts[2]  # секунды
            reminder_time = datetime(year, month, day, hour, minute, second)

            if reminder_time <= datetime.now():
                await update.message.reply_text("Ошибка: дата уже прошла. Введите будущую дату.")
                return

            # Сохраняем напоминание
            user_id = update.effective_user.id
            chat_id = update.effective_chat.id

            if user_id not in napminani:
                napminani[user_id] = []

            napminani[user_id].append({
                'текст': reminder_text,
                'время': reminder_time,
                'chat_id': chat_id
            })

            time_str = reminder_time.strftime("%y.%m.%d. %H:%M:%S")
            await update.message.reply_text(f" Напоминание установлено на {time_str}: {reminder_text}")

            delay = (reminder_time - datetime.now()).total_seconds()
            if delay > 0:
                asyncio.create_task(send_reminder(context, chat_id, delay, reminder_text))

        except (ValueError, IndexError):
            await update.message.reply_text("Ошибка: неверный формат даты или времени. Используйте формат: ГГ.ММ.ДД ЧЧ:ММ:СС")
            return

        # Сбрасываем состояние
        context.user_data.clear()
        return

    if text == "игра":
        await game(update, context)
        return
    elif text == "викторина":
        await viktorina(update, context)
        return

    # Обработка стандартных фраз
    for i in range(len(questions2[0])):
        if text in questions2[0][i] and questions2[1][i]:
            reply = random.choice(questions2[1][i])
            break

    await update.message.reply_text(reply)