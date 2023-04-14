import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
import aiogram
from loader import dp, db, bot
from keyboards.default.defaultbutton import main_menu

@dp.message_handler(CommandStart(),state="*")
async def bot_start(message: types.Message,state: FSMContext):
    await state.finish()
    name = message.from_user.full_name
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(id=message.from_user.id,name=name,language=message.from_user.language_code)
        await message.answer(f"Assalomu alaykum <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>!\n\nYordam: /help",reply_markup=main_menu)
        # Adminga xabar beramiz
        count = db.count_users()[0]
        if message.from_user.username is not None: 
            msg = f"Bazaga yangi foydalanuvchi qo'shildi\n🙎🏻‍♂️ Ismi: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n🆔 ID si: <code>{message.from_user.id}</code>\n✉️ Foydalanuvchi nomi: @{message.from_user.username}\n✡️ Telegram tili: {message.from_user.language_code}\n\nBazada {count} ta foydalanuvchi bor"
            await bot.send_message(chat_id=ADMINS[0], text=msg,parse_mode='HTML')
        else:
            msg = f"Bazaga yangi foydalanuvchi qo'shildi\n🙎🏻‍♂️ Ismi: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n🆔 ID si: <code>{message.from_user.id}</code>\n✡️ Telegram tili: {message.from_user.language_code}\n\nBazada {count} ta foydalanuvchi bor."
            await bot.send_message(chat_id=ADMINS[0], text=msg,parse_mode='HTML')

    except sqlite3.IntegrityError as err:
        if message.from_user.username is not None:
            await bot.send_message(chat_id=ADMINS[0], text=f"🙎🏻‍♂️ <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> bazaga oldin qo'shilgan\n✉️ Foydalanuvchi nomi: @{message.from_user.username}\n🆔 ID si: <code>{message.from_user.id}</code>\n✡️ Telegram tili: {message.from_user.language_code}",parse_mode='HTML')
        else:
            await bot.send_message(chat_id=ADMINS[0], text=f"🙎🏻‍♂️ <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> bazaga oldin qo'shilgan\n🆔 ID si: <code>{message.from_user.id}</code>\n✡️ Telegram tili: {message.from_user.language_code}",parse_mode='HTML')
        await message.answer(f"Assalomu alaykum <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>!\n\nYordam: /help",reply_markup=main_menu)

