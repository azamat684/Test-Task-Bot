"""

AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN AGAIN UNTIL I WON!

"""

#                             ZERIKISH TIME                             #


""" 

AGAIN AGAIN AGAIN AGAIN BUT YOU STILL DREAM NOT NULL TRY AGAIN UNTIL I WON #URAA

"""

from loader import dp,db,bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from states.state import taklif_user,ProductState
from data.config import ADMINS,CHANNELS
from keyboards.default.defaultbutton import product_menu,maxsulot_turlari,share_number,main_menu
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from keyboards.inline.inlinebutton import tasdiqlamoq,admin_confirm
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

#Xarid qilish bo'limi
@dp.message_handler(text="🛍 Xarid qilish",state="*")
async def taklif(message: types.Message,state: FSMContext):
    await state.finish()
    await message.reply("<b><i>Menyudan nima xarid qilmoqchiligizni tanlang</i></b>",parse_mode='HTML',reply_markup=product_menu)

@dp.message_handler(text='↩️ Orqaga',state="*")
async def back_main_menu(message: types.Message,state: FSMContext):  
    await state.finish()
    await message.answer("<b><i>Menyudan nima xarid qilmoqchiligizni tanlang</i></b>",parse_mode='HTML',reply_markup=product_menu)

@dp.message_handler(text='↩️ Orqaga',state=ProductState.products_contact)
async def back_type_product(message: types.Message,state: FSMContext):
    data = await state.get_data()
    maxsulot_type = data.get("maxsulot")
    await message.answer_photo(photo="https://ibb.co/17zFTGj",caption=f"<b><i>{maxsulot_type}-dan qaysi turdagisi kerak?</i></b>",reply_markup=maxsulot_turlari)

@dp.message_handler(text='↩️ Orqaga',state=ProductState.products_amount)
async def back_type_product3(message: types.Message,state: FSMContext):
    await message.answer("<b><i>Yaxshi,endi telefon raqamingizni jo'nating...\n\nPastda \"📞 Raqamni Jo'natish\" tugmasini bosing</i></b>",reply_markup=share_number)
      
    

@dp.message_handler(text="Kraska" ,state="*")
async def type_product1(message: types.Message,state: FSMContext):
    maxsulot = message.text
    await state.update_data({"maxsulot":maxsulot})
    data = await state.get_data()
    maxsulot_type = data.get("maxsulot")
    await message.reply_photo(photo="https://ibb.co/17zFTGj",caption=f"<b><i>{maxsulot_type}-dan qaysi turdagisi kerak?</i></b>",reply_markup=maxsulot_turlari)
    await ProductState.products.set()
  

  
@dp.message_handler(text="Qora",state=ProductState.products)
async def type_product2(message: types.Message,state: FSMContext):
    maxsulot_turi = message.text
    await state.update_data({"Maxsulot_turi" : maxsulot_turi})
    await message.reply(f"<b><i>Yaxshi,endi telefon raqamingizni jo'nating...\n\nPastda \"📞 Raqamni Jo'natish\" tugmasini bosing</i></b>",reply_markup=share_number)
    await ProductState.products_contact.set()
    

    
@dp.message_handler(content_types=['contact'],state=ProductState.products_contact)
async def user_contact(message: types.Message,state: FSMContext):
    contact = message.contact.phone_number
    
    await state.update_data({"raqami": contact})
    data = await state.get_data()
    maxsulot = data.get("maxsulot")
    maxsulot_turii = data.get("Maxsulot_turi")
    product_count= ReplyKeyboardMarkup(row_width=3)
    product_count.add(KeyboardButton(text="↩️ Orqaga"))
    for i in range(1,11):
        product_count.insert(KeyboardButton(text=i))
    await message.reply(f"<b><i>{maxsulot}</i></b> dan<b><i>{maxsulot_turii}</i></b> xilidan nechta buyurtma bermoqchisiz?",reply_markup=product_count)
    await ProductState.products_amount.set()
    
  


@dp.message_handler(state=ProductState.products_amount)
async def amount_product(message: types.Message,state: FSMContext):
    amount = message.text
    await state.update_data({"miqdori": amount})
    data = await state.get_data()
    product = data.get("maxsulot")
    product_type = data.get("Maxsulot_turi")
    product_amount = data.get("miqdori")
    raqami = data.get("raqami")
    await message.reply(f"🛍 Maxsulot nomi: <b>{product}</b>\n✨ Maxsulot turi: {product_type}\n🛒 Maxsulot miqdori: {product_amount}\n📞 Xaridorni telefon raqami: {raqami}\n\n💸 Umimiy xisob: <code>{product_amount} * 15000 so'm = {int(product_amount)*15000} so'm</code>\n\n<b><i>Siz bularni tasdiqlaysizmi?</i></b>",reply_markup=tasdiqlamoq)
    await ProductState.products_confirm.set()




@dp.callback_query_handler(text="ha",state=ProductState.products_confirm)
async def products_confirm(call: types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    product = data.get("maxsulot")
    product_type = data.get("Maxsulot_turi")
    product_amount = data.get("miqdori")
    raqami = data.get("raqami")
    #Foydalanuvchiga xabar yuborish
    await call.message.answer("<b><i>✅ Xaridingiz uchun raxmat tez orada siz bilan bog'lanamiz kuting... 😊</i></b>",reply_markup=main_menu)
    #Adminga xabar yuborish yangi zakaz xaqida
    if call.from_user.username is not None:
        for admins in ADMINS:
            await bot.send_message(chat_id=admins,text=f"<b><i>Bizga quyidagicha yangi buyurtma tushdi...!</i></b>\n\n🛍 Maxsulot: <b>{product}</b>\n🆕 Maxsulot turi: <b>{product_type}</b>\n🛒 Maxsulot miqdori: <b>{product_amount}</b>\n☎️ Xaridorni telefon raqami: <b>{raqami}</b>\n™️ Telegram foydalanuvchi nomi: @{call.from_user.username}\n\n💵 Umimiy xisob: <code>{product_amount} * 15000 so'm = {int(product_amount)*15000} so'm</code>\n\nPul to'ladimi?: <b>❌ Yo'q</b>",reply_markup=admin_confirm)
            # await ProductState.check_start.set()
    else:
        for admins in ADMINS:
            await bot.send_message(chat_id=admins,text=f"<b><i>Bizga quyidagicha yangi buyurtma tushdi...!</i></b>\n\n🛍 Maxsulot: <b>{product}</b>\n🆕 Maxsulot turi: <b>{product_type}</b>\n🛒 Maxsulot miqdori: <b>{product_amount}</b>\n☎️ Xaridorni telefon raqami: <b>{raqami}</b>\n™️ Telegram foydalanuvchi nomi: <a href='tg://user?id={call.from_user.id}'>{call.from_user.user}</a> \n\n💵 Umimiy xisob: <code>{product_amount} * 15000 so'm = {int(product_amount)*15000} so'm</code>\n\nPul to'ladimi?: <b>❌ Yo'q</b>",reply_markup=admin_confirm)
            # await ProductState.check_start.set()
    
@dp.callback_query_handler("to'landi",state="*")
async def check_admin_true(call: types.CallbackQuery,state: FSMContext):
    data = await state.get_data()
    product = data.get("maxsulot")
    product_type = data.get("Maxsulot_turi")
    product_amount = data.get("miqdori")
    raqami = data.get("raqami")
    if call.from_user.username is not None:
        await call.message.edit_text(f"<b><i>Bizga quyidagicha yangi buyurtma tushdi...!</i></b>\n\n🛍 Maxsulot: <b>{product}</b>\n🆕 Maxsulot turi: <b>{product_type}</b>\n🛒 Maxsulot miqdori: <b>{product_amount}</b>\n☎️ Xaridorni telefon raqami: <b>{raqami}</b>\n™️ Telegram foydalanuvchi nomi: @{call.from_user.username}\n\n💵 Umimiy xisob: <code>{product_amount} * 15000 so'm = {2*15000} so'm</code>\n\nPul to'ladimi?: <b>❌ Ha</b>")
        await state.finish()
    else:
        await call.message.edit_text(f"<b><i>Bizga quyidagicha yangi buyurtma tushdi...!</i></b>\n\n🛍 Maxsulot: <b>{product}</b>\n🆕 Maxsulot turi: <b>{product_type}</b>\n🛒 Maxsulot miqdori: <b>{product_amount}</b>\n☎️ Xaridorni telefon raqami: <b>{raqami}</b>\n™️ Telegramdagi nomi: @{call.from_user.full_name}\n\n💵 Umimiy xisob: <code>{product_amount} * 15000 so'm = {2*15000} so'm</code>\n\nPul to'ladimi?: <b>❌ Ha</b>")
        await state.finish()

#Adminning maxsulot uchun foydalanuvchi pul to'lagini tasdiqlash uchun inline tugma
# @dp.channel_post_handler()
# async def products_confirm7(call: types.CallbackQuery,state: FSMContext):
#     print(call.message.text)
#     print("salom ishladi2222222222222")
#     await call.message.delete()
#     data = await state.get_data()
#     product = data.get("maxsulot")
#     product_type = data.get("Maxsulot_turi")
#     product_amount = data.get("miqdori")
#     raqami = data.get("raqami")
#     #Adminga xabar yuborish yangi zakaz xaqida
#     if call.data == "to'landi":
#         print("salom ishladi")
#             # for channels in CHANNELS:
#             #     await bot.send_message(chat_id=call.message.id,text=f"<b><i>Bizga quyidagicha yangi buyurtma tushdi...!</i></b>\n\n🛍 Maxsulot: <b>{product}</b>\n🆕 Maxsulot turi: <b>{product_type}</b>\n🛒 Maxsulot miqdori: <b>{product_amount}</b>\n☎️ Xaridorni telefon raqami: <b>{raqami}</b>\n™️ Telegram foydalanuvchi nomi: @{call.from_user.username}\n\n💵 Umimiy xisob: <code>{product_amount} * 15000 so'm = {2*15000} so'm</code>\n\nPul to'ladimi?: <b>❌ Ha</b>")
#             #     await state.finish()
    
#         for channels in CHANNELS:
#             await bot.send_message(chat_id=channels,text=f"<b><i>Bizga quyidagicha yangi buyurtma tushdi...!</i></b>\n\n🛍 Maxsulot: <b>{product}</b>\n🆕 Maxsulot turi: <b>{product_type}</b>\n🛒 Maxsulot miqdori: <b>{product_amount}</b>\n☎️ Xaridorni telefon raqami: <b>{raqami}</b>\n™️ Telegram foydalanuvchi nomi: <a href='tg://user?id={call.from_user.id}'>{call.from_user.user}</a> \n\n💵 Umimiy xisob: <code>{product_amount} * 15000 so'm = {2*15000} so'm</code>\n\nPul to'ladimi?: <b>❌ Ha</b>")
#             await state.finish()


    
@dp.callback_query_handler(text="yo'q",state=ProductState.products_confirm)
async def products_confirm(call: types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    await call.message.answer("<b><i>❌ Xarid bekor qilindi...</i></b>",reply_markup = main_menu)
    await state.finish()
#Adminga taklif yozish
@dp.message_handler(text="✍🏻 Adminga yozish",state="*")
async def taklif(message: types.Message,state: FSMContext):
    await state.finish()
    # await call.message.edit_text("Taklifingizni yuboring,siz kiritgan taklif shaxsan Dilshod Abdullayevga boradi\n\n⚠️ Iltimos bexuda yozmang! O'zizni va boshqani <b>qadrli</b> vaqtini foydasiz narsaga sovurmang",parse_mode='HTML')
    await message.answer("Ismingiz va Familyangiz...?\n\nNamuna: <code>Sherbek Qo'chqorov</code>",parse_mode='HTML')
    await taklif_user.taklif_ismi.set()
    
#Userni malumotlarini olish
@dp.message_handler(state=taklif_user.taklif_ismi)
async def taklif2(message: types.Message,state: FSMContext):
    await state.update_data({"full_name": message.text})
    await state.update_data({"idsi":message.from_user.id})
    await message.reply(f"Yaxshi {message.text},endi taklifingizni yozing..!\n\n⚠️ Iltimos bexuda yozmang! O'zizni va boshqani <b>qadrli va qimmatli</b> vaqtini olmang!")
    await taklif_user.taklif_start.set()
    
#Userni taklifini ADMINGA yuborish
@dp.message_handler(state=taklif_user.taklif_start)
async def taklif2(message: types.Message,state: FSMContext):
    await message.reply("<b><i>Xabaringiz adminga yuborildi. Taklifingiz uchun tashakkur...!</i></b>")
    await state.update_data({"Taklif" : message.text})
    data = await state.get_data()
    ismi = data.get("full_name")
    taklifii = data.get("Taklif")
    idsii = data.get("idsi")
    if message.from_user.username is not None:
        await bot.send_message(chat_id=ADMINS[0],text=f"📬 Bizga yangi taklif kelib tushdi\n\n👤Kimdan: <a href='tg://user?id={idsii}'>{ismi}</a>\n⚡️ Telegram username: @{message.from_user.username}\n📨 Taklifi: <b>{taklifii}</b>",parse_mode='HTML')
        await state.finish()
    else:
        await bot.send_message(chat_id=ADMINS[0],text=f"📬 Bizga yangi taklif kelib tushdi\n\n👤Kimdan: <a href='tg://user?id={idsii}'>{ismi}</a>\n📨 Taklifi: <b>{taklifii}</b>",parse_mode='HTML')
        await state.finish()
        
    
    
    
#Ishlamay turgan funksiyalarga javob berish    
@dp.message_handler(lambda message: message.text in ["⚙️ Sozlamalar","ℹ️ Biz haqimizda"],state="*") 
async def al_datas(message: types.Message,state: FSMContext):
    await message.reply("❌ Hali bu fuksiya ishga tushmadi!") 
    await state.finish()

