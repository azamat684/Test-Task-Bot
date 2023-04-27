import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from data.config import ADMINS,CHANNELS
import aiogram
from loader import dp, db, bot
from keyboards.default.defaultbutton import main_menu
import aiogram.utils.markdown as fmt


@dp.message_handler(CommandStart(),state="*")
async def bot_start(message: types.Message,state: FSMContext):
    await state.finish()
    name = message.from_user.full_name
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(id=message.from_user.id,name=name,language=message.from_user.language_code)
        await message.answer(
        text=f"Assalomu alaykum <b><a href='tg://user?id={fmt.quote_html(message.from_user.id)}'>{fmt.quote_html(message.from_user.full_name)}</a></b>", 
        parse_mode=types.ParseMode.HTML,reply_markup=main_menu)
        # Adminga xabar beramiz
        count = db.count_users()[0]
        if message.from_user.username is not None: 
            msg = f"Bazaga yangi foydalanuvchi qo'shildi\n🙎🏻‍♂️ Ismi: <b>{fmt.quote_html(message.from_user.full_name)}</b>\n🆔 ID si: <code>{message.from_user.id}</code>\n✉️ Foydalanuvchi nomi: @{message.from_user.username}\n✡️ Telegram tili: {message.from_user.language_code}\n\nBazada {count} ta foydalanuvchi bor"
            await bot.send_message(chat_id=CHANNELS, text=msg,parse_mode='HTML')
        else:
            msg = f"Bazaga yangi foydalanuvchi qo'shildi\n🙎🏻‍♂️ Ismi: <b>{fmt.quote_html(message.from_user.full_name)}</b>\n🆔 ID si: <code>{message.from_user.id}</code>\n✡️ Telegram tili: {message.from_user.language_code}\n\nBazada {count} ta foydalanuvchi bor."
            await bot.send_message(chat_id=CHANNELS, text=msg,parse_mode='HTML')

    except sqlite3.IntegrityError as err:
        if message.from_user.username is not None:
            await bot.send_message(chat_id=CHANNELS, text=f"🙎🏻‍♂️ <b>{fmt.quote_html(message.from_user.full_name)}</b> bazaga oldin qo'shilgan\n✉️ Foydalanuvchi nomi: @{message.from_user.username}\n🆔 ID si: <code>{message.from_user.id}</code>\n✡️ Telegram tili: {message.from_user.language_code}",parse_mode='HTML')
        else:
            await bot.send_message(chat_id=CHANNELS, text=f"🙎🏻‍♂️ <b>{fmt.quote_html(message.from_user.full_name)}</b> bazaga oldin qo'shilgan\n🆔 ID si: <code>{message.from_user.id}</code>\n✡️ Telegram tili: {message.from_user.language_code}",parse_mode='HTML')
        await message.answer(text=f"Assalomu alaykum <b>{fmt.quote_html(message.from_user.full_name)}</b>",parse_mode=types.ParseMode.HTML,reply_markup=main_menu)
