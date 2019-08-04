import logging

from datetime import date, datetime
from telegram import TelegramError
from telegram.ext import ConversationHandler

from .models import Debot, session

logger = logging.getLogger(__name__)

#semuaAcara = session.query(Debot.jenis, Debot.nama, Debot.tanggal).all()

def acara(update, context):
    
    semuaAcara = session.execute("select jenis, nama, tanggal from debot", mapper=Debot)
    connection = session.connection(Debot)
    logging.info("mengecek acara")
    line = ''
    for x in semuaAcara:
        line += ' - '.join(str(i)for i in x)
        line += '\n'            

    update.message.reply_text(line)
    

def remind(context):
    
    job = context.job
    logger.info("memanggil remind")
    semuaAcara = session.execute("select jenis, nama, tanggal from debot", mapper=Debot)
    connection = session.connection(Debot)
    waktu = date.today()
    line = 'Jangan Lupa Ya Acara Selanjutnya Ada:\n\n'
    for x in semuaAcara:
        if waktu < x[2]:
            line += ' - '.join(str(i)for i in x)
            line += '\n'  
            
    
    context.bot.send_message(job.context, text=line)

def destroy(update, context):

    session.execute('''TRUNCATE TABLE debot''')
    session.commit()
    
    logger.info("Menghapus table")

    update.message.reply_text("Semua acara udah dihapus lurd!")
