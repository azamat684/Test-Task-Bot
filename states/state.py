from aiogram.dispatcher.filters.state import StatesGroup, State

class ProductState(StatesGroup):
    products = State()
    products_amount = State()
    products_contact = State()
    products_confirm = State()


class Reklama(StatesGroup):
    optional_reklama = State()
    
class taklif_user(StatesGroup):
    taklif_ismi = State()
    taklif_start = State()
    taklif_end = State()