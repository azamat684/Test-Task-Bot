from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from loader import db


main_menu = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
main_menu.add("🛍 Xarid qilish","✍🏻 Adminga yozish")
main_menu.add("⚙️ Sozlamalar","ℹ️ Biz haqimizda")

share_number = ReplyKeyboardMarkup(resize_keyboard=True)
share_number.add(KeyboardButton(text="📞 Raqamni Jo'natish",request_contact=True))
share_number.add(KeyboardButton(text="↩️ Orqaga"))

product_menu = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
product_menu.add('↩️ Orqaga')
all_products = db.select_all_products()
for product in all_products:
    product_menu.insert(product[1])

# product_menu.add('↩️ Orqaga',"Kraska","2-menu","3-menu","4-menu")

maxsulot_turlari = ReplyKeyboardMarkup(resize_keyboard=True)
maxsulot_turlari.add("↩️ Orqaga")
for product_type in all_products:
    maxsulot_turlari.insert(KeyboardButton(text=f"{product_type[2]}"))
    
# maxsulot_turlari.add("↩️ Orqaga","Qora")
# maxsulot_turlari.add("Oq","Jigarrang")

