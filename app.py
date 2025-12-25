#!/bin/python
import random
from http.cookiejar import user_domain_match

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackContext

TOKEN = "8260306943:AAFfchQLrtqoMUW91AJw6xgM3UXIOF7mdww"
GAME = False

# questions = [
#     [
#         "Сколько цветов в радуге?\na) пять\nb) восемь\nc) три\nd) семь",
#         "Столица Великобритании?\na) Париж \nb) Москва\nc) Каир\nd) Лондон",
#         "Сколько материков на Земле?\na) семь\nb) пять\nc) шесть\nd) восемь"
#     ],[
#         "d",
#         "d",
#         "c"
#     ]
# ]
# print(questions[0][0])
# print(questions[1][0])

questions2 = [
        [
            ["привет", "здравствуйте"],
            ["как дела?", "как дела"],
            ["пока", "досвидания"],
            ["что ты умеешь?", "что ты умеешь"]
        ],[
            ["И тебе привет", "Привет привет"],
            ["Всё хорошо, а твои?", "Да не оч. Как то грустно ботом работать :("],
            ["Пока пока. до скорых втреч!", "Бывай", "Проваливай"],
            ["я умею играть в камень ножницы бумага. Если хочешь сыграть нажми (/game)"]
        ]
    ]


#         reply = 'Я пока умею отвечать только на "привет", "здравствуйте", "как дела?", \
# "как дела", "пока" и "досвидания"'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Привет, {update.effective_user.first_name}!  Я твой бот. Чем могу помочь?")


async def greet_if_hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global GAME # говорю что переменная GAME не локальная а глобальная.
    # убрал update.message.text сделал переменную. 
    text = update.message.text.lower()
    # await update.message.reply_text(text) # дебаг. эхо вывод того что получил бот.
 

    # Если глобальная переменная GAME стоит в тру то вызываю функцию игра.
    # передаю туда полученный текст и выхожу, чтобы не спамить текстом болталки.
    if GAME:
        await update.message.reply_text(aktivi_game(text))
        return


    # смотрю длину массива. Прохожу циклом по вопросам и сравниваю с ответами.
    # если ответов больше 1 то отвечаю рандомно из ответов. 
    # если вопросов нет в масиве отвечаю дефолтный ответ.
    reply = 'Я пока умею отвечать только на "привет", "здравствуйте", "как дела?", \
"как дела", "пока" и "досвидания"' # дефолтный ответ. 
    for i in range(0, len(questions2[0])):
        if text in questions2[0][i]:
            if len(questions2[0][i]) == 0:
                reply = questions2[1][i]
            else:
                reply = (random.choice(questions2[1][i]))
    await update.message.reply_text(reply)


def aktivi_game(text):
    global GAME
    varianti = ["камень" , "ножницы" , "бумага"]
    if text not in varianti:
        # в случе ошибки специально не меняю глобальную гейм на фолс. Чтобы не вызывать игру снова.
        return "Ошибка, введите камень ножнцы или бумага"

    variant = random.choice(varianti)
    if text == variant:
        GAME = False
        return 'Я выбрал "' + variant + '". Ничья!'
    elif (text == "камень" and variant == "ножницы") \
    or (text == "ножницы" and variant == "бумага") \
    or (text == "бумага" and variant == "камень"):
        GAME = False
        return 'Я выбрал "' + variant + '". Ты победил!'
    else:
        GAME = False
        return 'Я выбрал "' + variant + '". Ты проиграл!'


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # context.user_data['game_igra'] = True # хз зачем это :) .
    await update.message.reply_text("Выбери камень ножницы или бумага")
    global GAME
    GAME = True
        
async def viktorina(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Отвечай на вопросы")
        

    # async def aktivi_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #     if not context.user_data.get('game_igra', False):
    #         return
    #     user = update.message.text.lower().strip()
    #     varianti = ['камень' , 'ножницы' , 'бумага']
    #     if user not in varianti:
    #         await update.message.reply_text( 'ошибка, введите камень ножнцы или бумага')
    #         return

    #     bot = random.choice(varianti)
    #     if user == bot:
    #         result ='Ничья!'
    #     elif (user == 'камень' and bot == 'ножницы') or (user == 'ножницы' and bot =='бумага') or (user == 'бумага' and bot == 'камень'):
    #         result ='Ты победил!'
    #     else:
    #         result ='Ты проиграл!'


app = ApplicationBuilder().token(TOKEN).build()
# Регистрация обработчиков
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("game", game))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greet_if_hello))
# Запуск бота
app.run_polling()
