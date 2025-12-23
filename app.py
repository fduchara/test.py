import random
from http.cookiejar import user_domain_match

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler, CallbackContext

questions = [
    'Сколько цветов в радуге?\na) пять\nb) восемь\nc) три\nd) семь',
    'Столица Великобритании?\na) Париж \nb) Москва\nc) Каир\nd) Лондон',
    'Сколько материков на Земле?\na) семь\nb) пять\nc) шесть\nd) восемь'
]

correct_answers = ['D', 'D','C']




async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет, {update.effective_user.first_name}!  Я твой бот. Чем могу помочь?')

async def greet_if_hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text.lower() in  ['привет', 'здравствуйте']:
        await update.message.reply_text(random.choice(['И тебе привет', 'Привет привет']))
    elif update.message.text.lower() in ['как дела?','как дела']:
        await update.message.reply_text('Всё хорошо, а твои?')
    elif update.message.text.lower() in ['пока' , 'досвидания']:
        await update.message.reply_text('Пока пока. до скорых втреч!')
    elif update.message.text.lower() in [ 'что ты умеешь?' , 'что ты умеешь']:
        await update.message.reply_text('я уменю играть в камень ножницы бумага. Если хочешь сыграть нажми (/game)')
    else:
        await update.message.reply_text(
            'Я пока умею отвечать только на "привет" , "здравствуйте" , "как дела?" , "как дела" ,"пока" и "досвидания"')


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['game_igra'] = True
    await update.message.reply_text('Выбери камень ножницы или бумага')

    async def aktivi_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not context.user_data.get('game_igra', False):
            return
        user = update.message.text.lower().strip()
        varianti = ['камень' , 'ножницы' , 'бумага']
        if user not in varianti:
            await update.message.reply_text( 'ошибка, введите камень ножнцы или бумага')
            return

        bot = random.choice(varianti)

        if user == bot:
            result ='Ничья!'
        elif (user == 'камень' and bot == 'ножницы') or (user == 'ножницы' and bot =='бумага') or (user == 'бумага' and bot == 'камень'):
            result ='Ты победил!'
        else:
            result ='Ты проиграл!'







app = ApplicationBuilder().token("8260306943:AAFfchQLrtqoMUW91AJw6xgM3UXIOF7mdww").build()

# Регистрация обработчиков
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("game", game))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greet_if_hello))

# Запуск бота
app.run_polling()
