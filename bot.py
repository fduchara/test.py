import logging
import random
import asyncio
from datetime import datetime
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler  # импорт для регестрации обработчика хандлер для лайн кнопок

TOKEN = "8420758526:AAHbHgvanf3pwtASdRA5MI4zkWw_RjtguHE"
GAME = False
VIKTORINA = False
VOPROS_INDEX = 0
ATTEMPS = 0
SIGRAN_RAUND = 0  # раунды
MAX_GAMES = 5  # макс раундов
POBEDA_BOT = 0  # победа бота
POBEDA_IGROK = 0  # победа игрока
napminani = {}


logging.basicConfig(level=logging.INFO)

questions = [
    [
        "Самое глубокое озеро в России?\na) Ладожское\nb) Хантайское\nc) Онежское\nd) Байкал",
        "Столица Великобритании?\na) Париж\nb) Москва\nc) Каир\nd) Лондон",
        "Сколько материков на Земле?\na) семь\nb) пять\nc) шесть\nd) восемь",
        "Сколько морей омывают Россию?\na) тринадцать\nb) семь\nc) четыре\nd) одиннадцать",
        "Какая планета Солнечной системы самая большая?\na) Земля\nb) Юпитер\nc) Сатурн\nd) Марс",
        "Какое животное является самым крупным на Земле?\na) Африканский слон\nb) Белый носорог\nc) Синий кит\nd) Кашалот",
        "Кто написал роман «Война и мир»?\na) Фёдор Достоевский\nb) Лев Толстой\nc) Антон Чехов\nd) Иван Тургенев",
        "Какой газ преобладает в атмосфере Земли?\na) Кислород\nb) Азот\nc) Углекислый газ\nd) Водород"
    ],
    [
        "b",
        "c",
        "a",
        "d",
        "c",
        "c",
        "b",
        "b"
    ]
]
questions2 = [
    [
        ["привет", "здравствуйте"],
        ["как дела?", "как дела"],
        ["пока", "досвидания"],
        ["расскажи шутку", "шутка", "расскажи анекдот"],
        ["что ты умеешь?", "что ты умеешь", "что ты умеешь?", "что ты умеешь"],
        ["плохо", "грустно"],
        ["весело", "хорошо"]
    ],
    [
        ["И тебе привет 😊", "Привет привет 👋"],
        ["Всё хорошо, а твои? 👍", "Да не оч. Как‑то грустно ботом работать :( 😔"],
        ["Пока‑пока! До скорых встреч! 👋", "Бывай! ✌️", "Проваливай! 😜"],
        [
            "Почему у часов нет друзей? Потому что они всё время торопят события!",
            "Почему компьютер иногда зависает? Он смотрит на ваши попытки разобраться в его ошибках и впадает в ступор.",
            "Почему дверь скрипит? — Она просто не согласна с вашим выбором.",
            "Почему кошка спит на клавиатуре? — Она редактирует ваш код ночью."
        ],
        [
            "Я умею играть в «камень‑ножницы‑бумага» ✂️🪨📄! Нажми /game, чтобы сыграть.\n"
            "Или /viktorina — запустить викторину 🏆️. Могу рассказать анекдот.\n"
            "Ещё могу поставить напоминание — нажми /reminder 🔔"
        ],
        ["Не грусти, держи подарок🎁", "Хочу поднять тебе настроение и рассказать шутку, просто напиши мне 'шутка'"],
        ["Рад, что у тебя всё хорошо", "если у тебя всё хорошо, то и у меня тоже"]
    ]
]

# кнопки
keyboard = [
    ["викторина", "игра"],
]
# клавиатура
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

game_keyboard = [
    ["камень", "ножницы", "бумага"],
    ["стоп"]
]
game_markup = ReplyKeyboardMarkup(game_keyboard, resize_keyboard=True)

viktrina_keyboard = [
    ["A", "B", "C", "D"],
    ["стоп"]
]
viktrina_markup = ReplyKeyboardMarkup(viktrina_keyboard, resize_keyboard=True)

line_keyboard = [
    [InlineKeyboardButton("имя", callback_data="name")],
    [InlineKeyboardButton("возраст", callback_data="age")],
    [InlineKeyboardButton("город", callback_data="address")]
]
reply_markup_line = InlineKeyboardMarkup(line_keyboard)

# подключила клавиатуру
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! Я твой бот. Чем могу помочь?",
        reply_markup=reply_markup
    )
    await update.message.reply_text(
        "давай знакомиться",
        reply_markup=reply_markup_line
    )

async def send_reminder(context: ContextTypes.DEFAULT_TYPE, chat_id: int, delay: float, text: str):
    if delay > 0:
        await asyncio.sleep(delay)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f" Напоминание: {text}"
        )

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
            year = date_parts[0]   # год
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

            if reminder_time >= datetime.now():
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

            time_str = reminder_time.strftime("%d.%m.%Y %H:%M:%S")
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
def aktivi_game(text):
    global GAME, SIGRAN_RAUND, MAX_GAMES, POBEDA_BOT, POBEDA_IGROK
    varianti = ["камень", "ножницы", "бумага"]

    if text not in varianti:
        return "❌ Ошибка, введите камень, ножницы или бумагу"

    variant = random.choice(varianti)
    SIGRAN_RAUND += 1

    if text == variant:
        result = f"Я быбрал '{variant}'Ничья! 🤝"
    elif (text == "камень" and variant == "ножницы") \
            or (text == "ножницы" and variant == "бумага") \
            or (text == "бумага" and variant == "камень"):
        POBEDA_IGROK += 1
        result = f"Я выбрал '{variant}' 🥇 Ты победил!"
    else:
        POBEDA_BOT += 1
        result = f"Я выбрал '{variant}' 😔 Ты проиграл!"

    if SIGRAN_RAUND >= MAX_GAMES:
        GAME = False
        if POBEDA_IGROK > POBEDA_BOT:
            return f"Я выбрал '{variant}'. Ты победил! 🥇\nСчёт: ты {POBEDA_IGROK}, бот {POBEDA_BOT}. Раундов: {SIGRAN_RAUND}/{MAX_GAMES}\n🎉 Ты победил!"
        elif POBEDA_IGROK < POBEDA_BOT:
            return f"Я выбрал '{variant}'. Ты проиграл! 😔\nСчёт: ты {POBEDA_IGROK}, бот {POBEDA_BOT}. Раундов: {SIGRAN_RAUND}/{MAX_GAMES}\n🤖 Бот победил!"
        else:
            return f"Я выбрал '{variant}'. Ничья! 🤝\nСчёт: ты {POBEDA_IGROK}, бот {POBEDA_BOT}. Раундов: {SIGRAN_RAUND}/{MAX_GAMES}\n🤝 Ничья!"
    else:
        return (f'{result} Счёт: ты {POBEDA_IGROK}, бот {POBEDA_BOT}. Раундов: {SIGRAN_RAUND}/{MAX_GAMES}')


def aktivi_viktrina(text):
    global VIKTORINA, VOPROS_INDEX, ATTEMPS
    otvet = questions[1][VOPROS_INDEX]
    max_attempts = 3

    if text == otvet:
        VOPROS_INDEX += 1
        ATTEMPS = 0
        if VOPROS_INDEX < len(questions[0]):
            return questions[0][VOPROS_INDEX]
        else:
            VIKTORINA = False
            VOPROS_INDEX = 0
            ATTEMPS = 0
            return "🎉 Викторина завершена!"
    else:
        ATTEMPS += 1
        remaining = max_attempts - ATTEMPS
        if remaining > 0:
            return f"❌ Неверно! Осталось {remaining} попыток"
        else:
            VIKTORINA = False
            return "Попытки исчерпаны. Программа завершена."


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


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Выбери камень, ножницы или бумагу. У нас будет 5 раундов.",
        reply_markup=game_markup
    )
    global GAME, SIGRAN_RAUND, POBEDA_BOT, POBEDA_IGROK
    GAME = True
    SIGRAN_RAUND = 0
    POBEDA_BOT = 0
    POBEDA_IGROK = 0


async def viktorina(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global VIKTORINA, VOPROS_INDEX, ATTEMPS
    VIKTORINA = True
    VOPROS_INDEX = 0
    ATTEMPS = 0
    await update.message.reply_text(
        "Я буду задавать вопросы с вариантами ответа. Отвечай только буквой. У тебя будет 3 попытки на ответ.",
        reply_markup=viktrina_markup
    )
    await update.message.reply_text(questions[0][VOPROS_INDEX])

async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Введите напоминание в формате: ГГ.ММ.ДД ЧЧ:ММ:СС Текст напоминания"
    )
    context.user_data['waiting_for_reminder'] = True


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("game", game))
app.add_handler(CommandHandler("viktorina", viktorina))
app.add_handler(CommandHandler("reminder", reminder))
app.add_handler(CallbackQueryHandler(line_button))  # этот обработчик обрабатывает именно нажатие лайн кнопок, поблема в том что срабатывает ее дефолтный ответ
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greet_if_hello))
app.run_polling()