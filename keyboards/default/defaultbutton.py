from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
main_menu.add("🛍 Xarid qilish","✍🏻 Adminga yozish")


product_menu = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
product_menu.add('↩️ Orqaga',"1-menu","2-menu","3-menu","4-menu")
