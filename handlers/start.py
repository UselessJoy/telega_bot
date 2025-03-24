from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.all_kb import main_kb, faq_kb, que_kb
from utils.utils import form_unread_message
from filters.regexp_filter import RegFilter
from decouple import config
from create_bot import bot
import re
from database import db
start_router = Router()

sn_reg = re.compile(r"^\d{6}$")
email_reg = re.compile(r"^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$")
unread_reg = re.compile(r"^У вас \d+ нов(?:ых|ое) сообщени(?:е|й|я)$")
class Question(StatesGroup):
    serial_number = State()
    email = State()
    question = State()

class Answer(StatesGroup):
    reply = State()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    kb = await main_kb(message.from_user.id)
    await message.answer('Выберите действие',
                         reply_markup=kb)

# @start_router.callback_query(F.data == 'faq_cb')
@start_router.message(F.text == '📝 Часто задаваемые вопросы')
                          # call: CallbackQuery
async def to_faq(message: Message):
    await message.answer("Что бы вы хотели узнать?", reply_markup=faq_kb())

# @start_router.callback_query(F.data == 'faq_cb')
@start_router.message(F.text == '📝Задать вопрос')
                          # call: CallbackQuery
async def set_question(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if not user:
      await message.answer("Введите серийный номер", reply_markup=que_kb())
      await state.set_state(Question.serial_number)
    else:
      await message.answer("Введите вопрос", reply_markup=que_kb())
      await state.set_state(Question.question)

@start_router.message(F.text == 'Назад')
async def back(message: Message):
    kb = await main_kb(message.from_user.id)
    await message.answer("Назад", reply_markup=kb)

@start_router.message(Question.serial_number, RegFilter(sn_reg))
async def proccess_serial_number(message: Message, state: FSMContext):
    await state.update_data(sn = message.text)
    await message.answer("Введите адрес электронной почты")
    await state.set_state(Question.email)

@start_router.message(Question.serial_number)
async def error_serial_number(message: Message, state: FSMContext):
    await message.answer("У серийного номера должно быть 6 цифр. Пожалуйста, повторите попытку")

@start_router.message(Question.email, RegFilter(email_reg))
async def proccess_email(message: Message, state: FSMContext):
    await state.update_data(em = message.text)
    await message.answer("Введите вопрос")
    await state.set_state(Question.question)

@start_router.message(Question.email)
async def error_email(message: Message, state: FSMContext):
    await message.answer("Некорректный адрес электронной почты. Пожалуйста, повторите попытку")

@start_router.message(Question.question)
async def process_question(message: Message, state: FSMContext):
    question_data = await state.get_data()
    user = await db.get_user(message.from_user.id)
    if not user:
        await db.insert_user(message.from_user.id, message.from_user.username, question_data['sn'], question_data['em'])
    else:
        question_data['sn'] = user[3]
        question_data['em'] = user[4]
    full_question = f"Серийный номер: {question_data['sn']}\nПочта: {question_data['em']}\nСообщение:\n{message.text}"
    
    topic_id = await db.get_user_topic(message.from_user.id)
    if not topic_id:
      topic = await bot.create_forum_topic(config('GROUP'), str(message.from_user.id))
      topic_id = topic.message_thread_id
      await db.update_topic(message.from_user.id, topic_id)
    await bot.send_message(chat_id = config('GROUP'), text = full_question, reply_to_message_id = topic_id[0])
    await state.clear()
    kb = await main_kb(message.from_user.id)
    await message.answer(f"Сообщение отправлено. Ожидайте ответа", reply_markup=kb)

@start_router.message(F.chat.type == 'supergroup')
async def from_supergroup(message: Message, state: FSMContext):
    if message.from_user.is_bot:
        return
    user_id = None
    try:
      user_id = int(message.reply_to_message.forum_topic_created.name)
    except Exception as e:
        print(f"Exception on partititon user_id: {e}")
        return
    kb_list = [
        [KeyboardButton(text="Прочитать")],
        [KeyboardButton(text="Назад")]
    ]
    kb = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
    )
    await db.insert_message(user_id, message.text)
    msg = await db.get_unread_messages(user_id)
    news_msg, msg_sending = form_unread_message(len(msg))
    await bot.send_message(user_id, f"У вас {len(msg)} {news_msg} {msg_sending}", reply_markup=kb)

@start_router.message(F.chat.type == 'private', F.text == 'Прочитать' or RegFilter(unread_reg))
async def continue_dialog(message: Message, state: FSMContext):
  unread_message = await db.get_unread_messages(message.from_user.id)
  if not unread_message:
      return
  for msg in unread_message:
      await message.answer(msg[0])
  await db.delete_unread_messages(message.from_user.id)
  await message.answer("Введите новое сообщение:", reply_markup=que_kb())
  await state.set_state(Answer.reply)

@start_router.message(Answer.reply)
async def proccess_reply(message: Message, state: FSMContext):
    to_topic = await db.get_user_topic(message.from_user.id)
    await bot.send_message(chat_id=config('GROUP'), text = message.text, reply_to_message_id = to_topic[0])
    await state.clear()
    kb = await main_kb(message.from_user.id)
    await message.answer(f"Сообщение отправлено. Ожидайте ответа", reply_markup=kb)