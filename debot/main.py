import logging

#library dateparser ternyata ada
import dateparser
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                        ConversationHandler)
from handlers.conversation import conv_handler
from handlers.misc import start, help, ups_handler, default
from handlers.remind import acara, destroy

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    """Start the bot."""
    updater = Updater("TOKEN", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    fallback_handler = MessageHandler(Filters.all, default)

    dp.add_handler(conv_handler)

    # on different commands - answer in Telegram
    dp.add_handler(start_handler)
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("acara", acara))
    dp.add_handler(CommandHandler("destroy", destroy))


    # special handler untuk errors
    dp.add_error_handler(ups_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
	main()
