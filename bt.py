import logging  # как поняла вместо print(), чтобы видеть ошибки если есть.
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackContext
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
TOKEN = "8420758526:AAHbHgvanf3pwtASdRA5MI4zkWw_RjtguHE"
GAME = False
VIKTORINA = False
VOPROS_INDEX = 0
ATTEMPS = 0


questions = [
   [
        "Самое глубокое озеро в России ?\na) Ладожское\nb) Хантайское\nc) Онежское\nd) Байкал",
        "Столица Великобритании?\na) Париж \nb) Москва\nc) Каир\nd) Лондон",
        "Сколько материков на Земле?\na) семь\nb) пять\nc) шесть\nd) восемь",
       "Суолько морей омывают Россию ?\na) тринадцать \nb) семь\nc) четыре\nd) одиннадцать"
    ],[
        "d",
        "d",
        "c",
        "a"
    ]
]

questions2 = [
    [
        ["привет", "здравствуйте"],
        ["как дела?", "как дела"],
        ["пока", "досвидания"],
        ["расскажи шутку","шутка","расскажи анекдот"],
        ["что ты умеешь?", "что ты умеешь","что ты умеешь?", "что ты умеешь"]
    ], [

        ["И тебе привет 😊", "Привет привет 👋"],
        ["Всё хорошо 👍", "Да не оч. Как‑то грустно ботом работать :( 😔"],
        ["Пока‑пока! До скорых встреч! 👋", "Бывай! ✌️", "Проваливай! 😜"],
        [
            "Почему у часов нет друзей? Потому что они всё время торопят события!",
            "Почему компьютер иногда зависает? Он смотрит на ваши попытки разобраться в его ошибках и впадает в ступор.",
            "Почему дверь скрипит? — Она просто не согласна с вашим выбором.",
            "Почему кошка спит на клавиатуре? — Она редактирует ваш код ночью."
        ],
        ["Я умею играть в «камень‑ножницы‑бумага» ✂️🪨📄! Нажми /game, чтобы сыграть. Или /viktorina — запустить викторину 🏆️"]
    ]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Привет, {update.effective_user.first_name}!  Я твой бот. Чем могу помочь?")


async def greet_if_hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global GAME, VIKTORINA, VOPROS_INDEX, ATTEMPS   # говорю что переменная  не локальная а глобальная.
    text = update.message.text.lower()

    # Если глобальная переменная GAME стоит в тру то вызываю функцию игра.
    # передаю туда полученный текст и выхожу, чтобы не спамить текстом болталки.
    if GAME:
        await update.message.reply_text(aktivi_game(text))
        return

    if VIKTORINA:
        otvet = questions[1][VOPROS_INDEX]
        max_attempts = 3

        if text == otvet:
            await update.message.reply_text("✅Верно!")
            VOPROS_INDEX += 1
            ATTEMPS = 0

            if VOPROS_INDEX < len(questions[0]):
                await update.message.reply_text(questions[0][VOPROS_INDEX])
            else:
                VIKTORINA = False
                VOPROS_INDEX = 0
                ATTEMPS = None
                await update.message.reply_text("🎉 Викторина завершена!")
        else:
            ATTEMPS += 1
            remaining = max_attempts - ATTEMPS

            if remaining > 0:
                await update.message.reply_text(f"❌Не верно! Осталось{remaining} попыток")
            else:
                VIKTORINA = False
                await update.message.reply_text("Попытки исчерпаны. Программа завершена.")

        return

# смотрю длину массива. Прохожу циклом по вопросам и сравниваю с ответами.
# если ответов больше 1 то отвечаю рандомно из ответов.
# если вопросов нет в масиве отвечаю дефолтный ответ.
    reply = 'Я пока не  умею отвечать  на такое.'  # дефолтный ответ.
    for i in range(0, len(questions2[0])):
        if text in questions2[0][i]:
            if len(questions2[0][i]) == 0:
                reply = questions2[1][i]
            else:
                reply = (random.choice(questions2[1][i]))
    await update.message.reply_text(reply)



def aktivi_game(text):
    global GAME
    varianti = ["камень", "ножницы", "бумага"]
    if text not in varianti:
        # в случе ошибки специально не меняю глобальную гейм на фолс. Чтобы не вызывать игру снова.
        return "❌Ошибка, введите камень ножнцы или бумага"

    variant = random.choice(varianti)
    if text == variant:
        GAME = False
        return 'Я выбрал "' + variant + '". Ничья!🤝'
    elif (text == "камень" and variant == "ножницы") \
            or (text == "ножницы" and variant == "бумага") \
            or (text == "бумага" and variant == "камень"):
        GAME = False
        return 'Я выбрал "' + variant + '". Ты победил!🥇'
    else:
        GAME = False
        return 'Я выбрал "' + variant + '". Ты проиграл!😔'


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Выбери камень ножницы или бумага")
    global GAME
    GAME = True

async def viktorina(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global VIKTORINA, VOPROS_INDEX, ATTEMPS
    VIKTORINA = True
    VOPROS_INDEX = 0
    ATTEMPS = 0
    await update.message.reply_text("Я буду задавать вопросы с вариантами ответа. отвечай только буквой")
    await update.message.reply_text(questions[0][VOPROS_INDEX])






app = ApplicationBuilder().token(TOKEN).build()
# Регистрация обработчиков
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("game", game))
app.add_handler(CommandHandler("viktorina", viktorina))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greet_if_hello))

app.run_polling()
