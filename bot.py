import logging
import random
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler    # импорт для регестрачии обработчика хандлер для лайн кнопок
TOKEN = "8420758526:AAHbHgvanf3pwtASdRA5MI4zkWw_RjtguHE"
GAME = False
VIKTORINA = False
VOPROS_INDEX = 0
ATTEMPS = 0
SIGRAN_RAUND = 0  # раунды
MAX_GAMES = 5     # макс раундов
POBEDA_BOT = 0    # победа бота
POBEDA_IGROK = 0  # победа игрока

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
        ["весело","хорошо"]
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
        ["Я умею играть в «камень‑ножницы‑бумага» ✂️🪨📄! Нажми /game, чтобы сыграть. Или /viktorina — запустить викторину 🏆️. Могу рассказать анекдот"],
        ["Не грусти, держи подарок🎁","Хочу поднять тебе настроение и рассказать шутку, просто напиши мне 'шутка'"],
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

# клавиатура
game_markup = ReplyKeyboardMarkup(game_keyboard, resize_keyboard=True)

# кнопки
viktrina_keyboard = [
    ["A", "B", "C", "D"],
    ["стоп"]
]
# клавиатура
viktrina_markup = ReplyKeyboardMarkup(viktrina_keyboard, resize_keyboard=True)

line_keyboard = [
    [InlineKeyboardButton("имя", callback_data="name")],
    [InlineKeyboardButton("возраст", callback_data="age")],
    [InlineKeyboardButton("город", callback_data="address")]
    ]
reply_markup_line = InlineKeyboardMarkup(line_keyboard)



#подключила клавиатуру
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Привет, {update.effective_user.first_name}! Я твой бот. Чем могу помочь?",
        reply_markup=reply_markup
    )
    await update.message.reply_text(
        "давай знакомиться",
        reply_markup=reply_markup_line
    )

async def greet_if_hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global GAME, VIKTORINA, VOPROS_INDEX, ATTEMPS, SIGRAN_RAUND, MAX_GAMES, POBEDA_BOT, POBEDA_IGROK
    text = update.message.text.lower()


    if GAME:
        await update.message.reply_text(aktivi_game(text))
        return

    if VIKTORINA:
        await update.message.reply_text(aktivi_viktrina(text))
        return

    reply = 'Я пока не умею отвечать на такое.'
    for i in range(0, len(questions2[0])):
        if text in questions2[0][i]:
            if len(questions2[0][i]) == 0:
                reply = questions2[1][i]
            else:
                reply = random.choice(questions2[1][i])
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

async def handle_buttons(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()
    user = update.message.text
    dannie = context.user_data.get('ozhidanie_otveta')  # получает данные от пользователя, get метод получения значения
    if dannie == 'name':
        context.user_data['ozhidanie_otveta'] = None
        await update.message.reply_text(
            f"приятно познакомиться, {user}! а я просто бот и у меня пока нет имени"
        )
        await update.message.reply_text("продолжим знакомсво",
                                        reply_markup=reply_markup_line
                                        )
    elif dannie == 'age':
        context.user_data['ozhidanie_otveta'] = None
        await update.message.reply_text(f"понял, тебе {user}",
                                        reply_markup=reply_markup_line
                                        )

    elif dannie == 'address':
        context.user_data['ozhidanie_otveta'] = None
        await update.message.reply_text(f"{user} - хороший город.",
                                        reply_markup=None)
        return

    if text == "стоп":
        global GAME, VIKTORINA
        GAME = False
        VIKTORINA = False
        await update.message.reply_text( 
            "Программа остановлена. пока",
              # reply_markup=ReplyKeyboardRemove() клава просто убирается после стопа
            reply_markup=reply_markup #клава возраается к первоначальному этапу
        )
        return

    if GAME:
        atvet = aktivi_game(text) 
        await update.message.reply_text(
            atvet,                        
            reply_markup=game_markup        
        )
        return

    if VIKTORINA:
        atvet  = aktivi_viktrina(text) 
        await update.message.reply_text(
            atvet,
            reply_markup=viktrina_markup
        )
        return

    if text == "игра":
        await game(update, context)
        return
    elif text == "викторина":
        await viktorina(update, context)
        return

    await greet_if_hello(update, context) 

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
             reply_markup = game_markup
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
            reply_markup = viktrina_markup
    )
    await update.message.reply_text(questions[0][VOPROS_INDEX])

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("game", game))
app.add_handler(CommandHandler("viktorina", viktorina))
app.add_handler(CallbackQueryHandler(line_button))   # этот обработчик обрабатывает именно нажатие лайн кнопок, поблема в том что срабатывает ее дефолтный ответ
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greet_if_hello))
app.run_polling()
