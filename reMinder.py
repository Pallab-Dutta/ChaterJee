import time
import datetime
import telegram 
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters                                                                                                         

TOKEN = '1711613332:AAHzf0GMQPjnBINOfIhfbK9dmIUo7mHiThw'                                                                                                                                              
pratyasha = '1149912690'
pallab    = '1651529355'
BOT = telegram.Bot(token=TOKEN)                                                                                                                                                                       

msg = """
Don't worry I will remind you to drink water on time.
                                                - vutuBot

from your's ever Pallab da
"""

#BOT.sendMessage(chat_id=pratyasha, text=msg)
BOT.sendMessage(chat_id=pallab, text=msg)
n = 2 #minutes
morning = datetime.datetime(2022,7,21,7,30,00)
night = datetime.datetime(2022,7,21,11,25,00)
reset = datetime.datetime(2022,7,21,11,30,00)

while True:
    now=datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    if now > morning and now < night:
        print('if')
        #BOT.sendMessage(chat_id=pratyasha, text='%s - Drink some water!'%(current_time))
        BOT.sendMessage(chat_id=pallab, text='%s - Drink some water!'%(current_time))
        time.sleep(60*n)
    elif now==reset:
        print('elif')
        morning = morning + datetime.timedelta(days=1)
        night = night + datetime.timedelta(days=1)
        reset = reset + datetime.timedelta(days=1)
        print(morning,night,reset)
        time.sleep(60)
