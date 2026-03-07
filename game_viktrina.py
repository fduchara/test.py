import random
from data import  questions

VOPROS_INDEX = 0
ATTEMPS = 0
SIGRAN_RAUND = 0
MAX_GAMES = 5
POBEDA_BOT = 0
POBEDA_IGROK = 0

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

def aktivi_viktrina(text, context):
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

