import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from states.state import Reklama,add_maxsulot
from aiogram.dispatcher import FSMContext
from keyboards.inline.inlinebutton import button_for_admins,button_for_admins_back
from aiogram.types import CallbackQuery,Message

@dp.message_handler(commands="/panel")
async def admin_panel(message: types.Message,state: FSMContext):
    await message.answer("<b><i>Admin panelga xush kelibsiz!\nSiz quyidagi buyruqlarni bajara olasiz...</i></b>\n\n<b>Botdan foydalanuvchilar sonini ko'ra olasiz\nO'sha foydalanuvchilarga reklama (xabar) yubora olasiz\nSotuvdagi maxsulotlaringizga yangi maxsulot qo'sha olasiz\nVa o'sha maxsulotlardan birisini o'chira olasiz!</b>",reply_markup=button_for_admins)
    await state.finish()

@dp.callback_query_handler(text="back_panel",state="*")
async def count_users(call: types.CallbackQuery,state: FSMContext):
    await call.message.edit_text("<b><i>Admin panelga xush kelibsiz!\nSiz quyidagi buyruqlarni bajara olasiz...</i></b>\n\n<b>Botdan foydalanuvchilar sonini ko'ra olasiz\nO'sha foydalanuvchilarga reklama (xabar) yubora olasiz\nSotuvdagi maxsulotlaringizga yangi maxsulot qo'sha olasiz\nVa o'sha maxsulotlardan birisini o'chira olasiz!</b>",reply_markup=button_for_admins)
    await state.finish()

@dp.callback_query_handler(text="count_users")
async def count_users(call: types.CallbackQuery):
    user_count = db.count_users()[0]
    await call.answer(text=f"Botdan foydalanuvchilar soni {user_count} ta!",show_alert=True)


@dp.callback_query_handler(text="reklama",state="*")
async def share_reklama(call: types.CallbackQuery,state: FSMContext):
    await call.message.edit_text(text="Menga reklama uchun ixtiyoriy xabar jo'nating va men uni foydalanuvchilarga jo'nataman.",reply_markup=button_for_admins_back)
    await Reklama.optional_reklama.set()
    
  
@dp.message_handler(state=Reklama.optional_reklama)
async def send_reklama(message: types.Message, state: FSMContext):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        try:
            await message.send_copy(chat_id=user_id)
            await asyncio.sleep(0.05)
        except Exception as excep:
            await message.answer(f"{user[1]} botni bloklagani uchun unga reklama bormadi")



@dp.callback_query_handler(text="maxsulot_qoshish",state="*")
async def add_product(call: types.CallbackQuery,state: FSMContext):
    await call.message.edit_text(text="<b>*********BU SHART!*********</b>\nQo'shmoqchi bo'lgan maxsulotingizni nomini yozing...",reply_markup=button_for_admins_back)
    await add_maxsulot.maxsulot_nomi.set()
    
@dp.message_handler(state=add_maxsulot.maxsulot_nomi)
async def add_maxsulot_nomi(message: Message,state: FSMContext):
    name_product = message.text
    await state.update_data({"nomi":name_product})
    await message.reply("<b>*********BU SHART!*********</b>\nO'sha maxsulot turini kiriting...")
    await add_maxsulot.maxsulot_turi.set()
    

@dp.message_handler(state=add_maxsulot.maxsulot_turi)
async def add_maxsulot_nomi(message: Message,state: FSMContext):
    type_product = message.text
    await state.update_data({"turi":type_product})
    await message.reply("<b>*********BU SHART!*********</b>\nO'sha maxsulot miqdorini kiriting...\nEng maksimum <b>10</b>")
    await add_maxsulot.maxsulot_miqdori.set()
    
@dp.message_handler(state=add_maxsulot.maxsulot_miqdori)
async def add_maxsulot_nomi(message: Message,state: FSMContext):
    amount_product = message.text
    await state.update_data({"miqdori":amount_product})
    data = await state.get_data()
    
    nomi = data.get("nomi")
    turi = data.get("turi")
    miqdori = data.get("miqdori")
    
    
    try:
        db.add_product(product_name=nomi,product_type=turi,product_count=miqdori)
        #Maxsulot bazaga muvvofaqiyatli qo'shildi
        await message.reply("<b>Ajoyib! Maxsulot sotuvga chiqdi.\nTekshirib ko'rish uchun /start bosib <i>🛍 Xarid qilish</i> bo'limini ko'ring</b>",reply_markup=button_for_admins_back)
        await state.finish()
    except Exception as err:
        print(f"Xato chiqdi: {err}")
    
    

@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    id = []
    name = []
    for user in users:
        name.append(user[1])
    data = {"Name": name}
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
       
@dp.message_handler(text="/reklama", user_id=ADMINS, state="*")
async def optional_ad(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Menga reklama uchun ixtiyoriy xabar jo'nating va men uni foydalanuvchilarga jo'nataman.")
    await Reklama.optional_reklama.set()



@dp.message_handler(text="/count",user_id = ADMINS)
async def count(message: types.Message):
    user_count = db.count_users()[0]
    await message.answer(f"Bazada <b>{user_count}</b> da foydalanuvchi bor")

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")
