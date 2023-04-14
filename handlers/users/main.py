from loader import dp,db,bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from states.state import taklif_user,ProductState
from data.config import ADMINS
from keyboards.default.defaultbutton import product_menu
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
#Xarid qilish bo'limi
@dp.message_handler(text="🛍 Xarid qilish",state="*")
async def taklif(message: types.Message,state: FSMContext):
    await state.finish()
    await message.reply("<b><i>Menyudan nima xarid qilmoqchilignizni tanlang<i></b>",parse_mode='HTML',reply_markup=product_menu)
    await ProductState.products.set()
    
    
@dp.message_handler(state=ProductState.products)
async def taklif(message: types.Message,state: FSMContext):
    await state.finish()
    
    inline_markup = InlineKeyboardMarkup(row_width=3)
    for i in range(1,11):
        inline_markup.insert(InlineKeyboardButton(text=i))
    await message.reply("Nechta buyurtma bermoqchisiz?",reply_markup=inline_markup)
    await ProductState.p
        

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
    await message.reply("Taklifingiz uchun tashakkur 😊")
    await state.update_data({"Taklif" : message.text})
    data = await state.get_data()
    ismi = data.get("full_name")
    taklifii = data.get("Taklif")
    idsii = data.get("idsi")
    await bot.send_message(chat_id=ADMINS[0],text=f"📬 Bizga yangi taklif kelib tushdi\n\n👤Kimdan: <a href='tg://user?id={idsii}'>{ismi}</a>\n📨 Taklifi: <b>{taklifii}</b>",parse_mode='HTML')
    await state.finish()
    
    
#Ishlamay turgan funksiyalarga javob berish    
@dp.message_handler(lambda message: message.text in ["4-menu"]) 
async def al_datas(message: types.Message):
    await message.reply("❌ Hali bu fuksiya ishga tushmadi!") 

