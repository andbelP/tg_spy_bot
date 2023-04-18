from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher,executor,types
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked
from config import TOKEN
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import random
import asyncio
import time
from aiogram.dispatcher import FSMContext
from datetime import datetime
from keyboards import b1,b2,b3
from aiogram.utils.helper import Helper, HelperMode, ListItem
bot=Bot(TOKEN)
storage=MemoryStorage()
dp=Dispatcher(bot=bot, storage=storage)
scheduler=AsyncIOScheduler()
data=0
from vk_parse.vk_parsing import getOnline

#----------------------------------------------on_startup, on_shutdown, botblocked---------------------------------
async def shutdown(dp):

    await bot.close()

async def on_startup(_):
    print('ALL GOOD')


@dp.errors_handler(exception=BotBlocked)
async def bot_block(update:types.Update,exception:BotBlocked)-> bool:
    print('Нельзя отправить сообщение потому что нас заблокировали')
    return True
#/////////////////////////////////////////////////////////////////////////////////////////////////////////////




#----------------------------------------------KEYBOARDS-----------------------------------------------
def get_cancel()->ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(b2)
    return kb

def get_kb()->ReplyKeyboardMarkup:
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(b3).add(b1)
    return kb

#//////////////////////////////////////////////////////////////////////////////////////////////
class getOnlineState(StatesGroup):
    cmnd=State()
b=1
last_seen=1
async def checkOnline(msg,text):
    if(dict(list(getOnline(text))[0])['online']==1):
        last_seen=datetime.now()
        await msg.answer(last_seen)




@dp.message_handler(commands='start')
async def start(msg:types.Message):
    await msg.answer('Привет. Напиши /help чтобы ознакомиться с командами',reply_markup=get_kb())


@dp.message_handler(commands='setonline',state=None)
async def getonlinee(msg:types.Message):
    await msg.answer('Напиши короткое имя пользователя (например andbelorig), за которым нужно следить')
    await getOnlineState.cmnd.set()


@dp.message_handler(state=getOnlineState.cmnd)
async def send_result_online(msg:types.Message,state:FSMContext):
    text=msg.text

    await msg.answer('Отлично. Теперь, когда пользователь будет онлайн вы узнаете об этом',reply_markup=get_cancel())
    scheduler.add_job(checkOnline,"interval",seconds=5,args=(msg,text))
    await state.finish()


@dp.message_handler(commands='cancelonline')
async def cancel_online(msg:types.Message):
    scheduler.shutdown()
    await msg.answer('Слежка за пользователем отменена',reply_markup=get_kb())

@dp.message_handler(commands='help')
async def send_help(msg:types.Message):
    await msg.reply('Данный бот следит за пользователем ВК, и если пользователь онлайн отправляет вам сообщение раз в 5 секунд'
                    '/help - помощь'
                    '/setonline - начать вести слежку за пользователем'
                    '/cancelonline - отменить слежку за пользователем')






if __name__=='__main__':
    scheduler.start()
    executor.start_polling(dp,on_startup=on_startup,skip_updates=True,on_shutdown=shutdown)



