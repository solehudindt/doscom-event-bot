import logging
import random

from telegram.error import (TelegramError, BadRequest)
from telegram.ext import ConversationHandler


logger = logging.getLogger(__name__)


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Hello gengs!! \n'
                              f'Gue Debot, Doscom Event Bot\n'
                              f'Semoga kehadiran gue bisa membantu,\n'
                              f'Yang mau kontribusi biar gue tambah pinter bisa contact @solehudindt\n'
                              f'\n'
                              f'/help buat cari tau command')


def ups_handler(update, context):
    try:
        raise context.error
    except BadRequest:
        logger.exception("Ada error di Telegram")
        update.effective_message.reply_text('Ada yang error ¯\\_(ツ)_/¯, Apakah acara kosong?')
    except TelegramError:
        logger.exception("Ada error di Telegram")
        update.effective_message.reply_text('Ada yang error ¯\\_(ツ)_/¯')
    except Exception:
        logger.exception("Ada yang error nih")
        update.effective_message.reply_text('Ada yang error ¯\\_(ツ)_/¯')

def default(update, context):
    """If a user sends an unknown command, answer accordingly. But not always to avoid flooding"""
    if random.choice((0, 1)):
        context.bot.send_message(
            chat_id=update.effective_message.chat_id,
            text="Gue ngga paham 🧐.. /help buat cari tau command"
        )

def help(update, context):
    """Send a message when the command /help is issued."""
    text = (f"» *Ini gengs commandnya :*\n"
                f"/start  Buat nampilin start\n"
                f"/help   Buat nampilin command tersedia\n"
                f"/input  Buat input acara\n"
                f"/cancel Buat batal input\n"
                f"/acara  Buat nampilin acara\n"
                f"/destroy  Buat hapus semua acara\n"
    )
    update.message.reply_text(text)