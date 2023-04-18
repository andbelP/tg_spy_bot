from aiogram import Bot, Dispatcher,executor,types
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup
from config import TOKEN
import random

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1=KeyboardButton('/setonline')
b2=KeyboardButton('/cancelonline')
b3=KeyboardButton('/help ')

