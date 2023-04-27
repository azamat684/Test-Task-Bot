from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup


tasdiqlamoq = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Ha",callback_data='ha'),InlineKeyboardButton(text="❌ Bekor qilish",callback_data="yo'q")]
])

admin_confirm = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ To'landi",callback_data="to'landi")]
])


button_for_admins = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="👤 A'zolar soni",callback_data='count_users'),InlineKeyboardButton(text="#️⃣ Reklama",callback_data='reklama')],
    [InlineKeyboardButton(text="🛍 Maxsulot qo'shish",callback_data='maxsulot_qoshish'),InlineKeyboardButton(text="🪓 Maxsulot o'chirish",callback_data="maxsulot_ochirish")]
])

button_for_admins_back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="↩️ Orqaga",callback_data='back_panel')]
])