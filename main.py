import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

reply_keyboard = [['/play', '/settings'],
                  ['/rules', '/close']]
play_kb = [['/close']]
candies = 50
step = 15

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
mark_play = ReplyKeyboardMarkup(play_kb, one_time_keyboard=False)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5703944288:AAGYgnvlzKtXmFkBmBfML6YKIX-NHGvUtr0'


def start(update, context):
    name = f"{update.message.from_user.first_name} {update.message.from_user.last_name}"
    update.message.reply_text(
        f"Привет, {name}! Давай поиграем",
        reply_markup=markup
    )

def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=markup
    )

def rules(update, context):
    update.message.reply_text(
        "в начале игры нужно определить количество конфет на кону, и максимальное количество конфет которое можно взять за один раз.")


def settings(update, context):
    update.message.reply_text("Введите общее количество конфет на кону и максимальное количество на 1 ход")
    return 1

def set_settings(update, context):
    global candies
    global step
    size = str(update.message.text).split()
    candies = int(size[0])
    step = int(size[1])
    update.message.reply_text("правила установлены.")
    return ConversationHandler.END

def play(update, context):
    update.message.reply_text(f"На кону {candies} конфет. Ваш ход. Сколько возьмёте конфет? Не больше {step} ", reply_markup = mark_play)
    return 1 

def play_step(update, context):
    global candies
    candy = int(update.message.text)
    candies -= candy
    if candies <= step:
        update.message.reply_text("ХА-ХА-ХА ТЫ ПРОИГРАЛ!", reply_markup=markup)

        return ConversationHandler.END
    else:
        update.message.reply_text(f". Я взял {candies % (step + 1)} конфет. Осталось {candies - candies % (step + 1)}")
        candies -= candies % (step + 1)
        if candies <= step:

            update.message.reply_text(" я проиграл (", reply_markup=markup)
            return ConversationHandler.END
        
      

            
def stop(update, context):
    update.message.reply_text("Всё! Пока!")
    return ConversationHandler.END



def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    settings_hundler = ConversationHandler (
    entry_points=[CommandHandler('settings',settings)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, set_settings)],
        
    },
    fallbacks=[CommandHandler('stop', stop)]
    
    )
    dp.add_handler(settings_hundler)

    play_hundler = ConversationHandler (
    entry_points=[CommandHandler('play',play)],
    states={
        1: [MessageHandler(Filters.text & ~Filters.command, play_step)],
    },
    fallbacks=[CommandHandler('stop', stop)]
    )  
    dp.add_handler(play_hundler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rules", rules))

    dp.add_handler(CommandHandler("close", close_keyboard))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()