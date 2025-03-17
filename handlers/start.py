from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.all_kb import main_kb, faq_kb, que_kb
from filters.regexp_filter import RegFilter
from decouple import config
from create_bot import bot
import re
start_router = Router()

sn_reg = re.compile(r"^\d{6}$")
email_reg = re.compile(r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$")
class Question(StatesGroup):
    serial_number = State()
    email = State()
    question = State()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Выберите действие',
                         reply_markup=main_kb())

# @start_router.callback_query(F.data == 'faq_cb')
@start_router.message(F.text == '📝 Часто задаваемые вопросы')
                          # call: CallbackQuery
async def to_faq(message: Message):
    await message.answer("Что бы вы хотели узнать?", reply_markup=faq_kb())

# @start_router.callback_query(F.data == 'faq_cb')
@start_router.message(F.text == '📝Написать вопрос')
                          # call: CallbackQuery
async def set_question(message: Message, state: FSMContext):
    # Устанавливаем пользователю состояние "выбирает вопрос"
    await message.answer("Введите серийный номер", reply_markup=que_kb())
    await state.set_state(Question.serial_number)

@start_router.message(F.text == 'Назад')
async def back(message: Message):
    await message.answer("Назад", reply_markup=main_kb())

@start_router.message(Question.serial_number, RegFilter(sn_reg))
async def proccess_serial_number(message: Message, state: FSMContext):
    await state.update_data(sn=message.text)
    await message.answer("Введите адрес электронной почты")
    await state.set_state(Question.email)

@start_router.message(Question.serial_number)
async def error_serial_number(message: Message, state: FSMContext):
    await message.answer("У серийного номера должно быть 6 цифр. Пожалуйста, повторите попытку")

@start_router.message(Question.email, RegFilter(email_reg))
async def proccess_email(message: Message, state: FSMContext):
    await state.update_data(em=message.text)
    await message.answer("Введите вопрос")
    await state.set_state(Question.question)

@start_router.message(Question.email)
async def error_email(message: Message, state: FSMContext):
    await message.answer("Некорректный адрес электронной почты. Пожалуйста, повторите попытку")

@start_router.message(Question.question)
async def process_question(message: Message, state: FSMContext):
    question_data = await state.get_data()
    full_question = f"Серийный номер: {question_data['sn']}\nПочта: {question_data['em']}\nСообщение:\n{message.text}"
    await bot.send_message(config('GROUP'), full_question)
    await message.answer(f"Сообщение отправлено", reply_markup=main_kb())
    await state.clear()