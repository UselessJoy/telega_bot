from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_kb():
    kb_list = [
        [KeyboardButton(text="📝Написать вопрос", callback_data='get_person')],
        [KeyboardButton(text="📖 Часто задаваемые вопросы", callback_data='faq_cb')]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True
    )
    return keyboard

def faq_kb():
    kb_list = [
        [KeyboardButton(text="У меня часто возникает timer_too_close", callback_data='timer_too_close')],
        [KeyboardButton(text="Пишет \"Принтер готов\", но дальше ничего не происходит", callback_data='not_init')],
        [KeyboardButton(text="Не могу подключиться к принтеру через его точку доступа", callback_data='ap_connect')],
        [KeyboardButton(text="Выскакивает ошибка mcu", callback_data='why_so_expensive')],
        [KeyboardButton(text="Могу ли я модернизировать прошивку?", callback_data='can_modern')],
        [KeyboardButton(text="Что делать, если возникает ошибка конфигурации?", callback_data='can_modern')],
        [KeyboardButton(text="У меня все сломалось! Памагите!!!", callback_data='full_shit')],
        [KeyboardButton(text="Закрыть", callback_data='full_shit')],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
    )
    return keyboard

def que_kb():
    kb_list = [
        [KeyboardButton(text="Назад")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
    )
    return keyboard