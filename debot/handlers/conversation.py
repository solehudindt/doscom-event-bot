#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from mysql.connector.errors import DataError
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from datetime import datetime, timedelta
from .models import Debot, session
from .remind import remind

import dateparser
import logging

logger = logging.getLogger(__name__)

val = []
JENIS, NAMA, TANGGAL = range(3)

def input(update, context):
    logger.info('input acara')
    reply_keyboard = [['RKT', 'NON-RKT']]

    update.message.reply_text(
        'Masukan jenis acaranya gengs?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return JENIS

def jenis(update, context):
    user = update.message.from_user
    logger.info("Jenis acara : %s", update.message.text)
    val.append(str(update.message.text))
    update.message.reply_text('Okay noted! Silahkan masukan nama acara.',
                              reply_markup=ReplyKeyboardRemove())

    return NAMA

def nama(update, context):
    user = update.message.from_user
    logger.info("Nama acara : %s", update.message.text)
    val.append(str(update.message.text))
    update.message.reply_text('Sekarang masukin tanggalnya. format <yyyy-mm-dd>',
                              reply_markup=ReplyKeyboardRemove())

    return TANGGAL

def tanggal(update, context):
    user = update.message.from_user
    due = dateparser.parse(update.message.text)
    tgl = update.message.text.split('-')
    chat_id = update.message.chat_id
    waktu = datetime.now()
    
    try:
        if waktu < due:
            if int(tgl[1]) > 12 or int(tgl[2]) > 31 :
                logger.info("Tangal berlebih")
                update.message.reply_text("Maaf format tanggal salah, silahkan /input lagi")
                val.clear()
            else:
                logger.info("Tanggal acara : %s", update.message.text)
                val.append(str(update.message.text))
                # sql = "INSERT INTO acara (id, jenis, nama, tanggal) VALUES (%s, %s, %s, %s)"
                new_acara = Debot(jenis=val[0], nama=val[1], tanggal=val[2])
                session.add(new_acara)
                session.commit()
                
                update.message.reply_text('Terimakasih semoga membantu.')


                # Create the reminder
                diff = timedelta(days=-30, hours=12)
                due += diff
                logger.info("menambah reminder %s", due)
                job = context.job_queue.run_once(remind, due, context=chat_id)
        else:
            logger.info("Lupa tanggal")
            val.clear()
            update.message.reply_text("Lupa tanggal boss? ¯\\_(ツ)_/¯, /input lagi")

    except (IndexError, ValueError, TypeError, DataError):
        logger.info("Input tangal error")
        update.message.reply_text("Salah input tanggal, Silahkan /input lagi")
        val.clear()

    return ConversationHandler.END

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    val.clear()
    update.message.reply_text('Okay, siap lurd.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('input', input)],

        states={
            JENIS: [MessageHandler(Filters.regex('^(RKT|NON-RKT)$'), jenis)],

            NAMA: [MessageHandler(Filters.text, nama)],

            TANGGAL: [MessageHandler(Filters.text, tanggal)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )