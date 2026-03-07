import asyncio
from telegram.ext import ContextTypes
from telegram import Update


async def send_reminder(context: ContextTypes.DEFAULT_TYPE, chat_id: int, delay: float, text: str):
    if delay > 0:
        await asyncio.sleep(delay)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f" Напоминание: {text}"
        )

async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Введите напоминание в формате: ГГ.ММ.ДД ЧЧ:ММ:СС Текст напоминания"
    )
    context.user_data['waiting_for_reminder'] = True


