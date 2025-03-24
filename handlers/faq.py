from aiogram import F, Router
from aiogram.types import Message
from keyboards.all_kb import faq_kb, main_kb
faq_router = Router()

@faq_router.message(F.text == 'У меня часто возникает timer_too_close')
async def send_timer_too_close(message: Message):
  formatted_message = (
      "Если у вас часто возникает ошибка Timer too close, то, в первую очередь, "
      "необходимо повторно откалибровать положение концевика Z и пробы. "
      "Если это не помогает, то попробуйте в файле конфигурации поставить "
      "в секции [printer] значение max_accel меньше, чем указано в конфиге (к примеру, на 5000) "
      "и попробуйте отслайсить gcode на меньших скоростях. "
      "В случае, если ошибка остается, то тогда необходимо обратиться в сервисный центр"
  )
  await message.answer(formatted_message, reply_markup=faq_kb())

@faq_router.message(F.text == 'Пишет \"Принтер готов\", но дальше ничего не происходит')
async def send_not_init(message: Message):
  formatted_message = (
      "Чаще всего проблема возникает если произошла какая-либо ошибка во время инициалиазции ПО. "
      "Зачастую это может происходить из-за отсутствия поля формата serial: usb_klipper_xxx в секции [mcu]"
      "Если у вас возникает эта проблема - просьба скинуть нам лог через сервисы KS или fluidd"
  )
  await message.answer(formatted_message, reply_markup=faq_kb())

@faq_router.message(F.text == 'Не могу подключиться к принтеру через его точку доступа')
async def send_ap_connect(message: Message):
  formatted_message = (
      "Есть некоторая проблема соединения телефона с точкой доступа (далее - ТД) принтера. "
      "Эта ошибка свойственна только для телефонов с определенной версией Android и IOS. "
      "Если у вас возникает эта ошибка, то тогда вам необходимо запускать ТД без пароля"
      "Мы стараемся решить эту проблему"
  )
  await message.answer(formatted_message)

@faq_router.message(F.text == 'Выскакивает ошибка mcu')
async def send_why_so_expensive(message: Message):
  formatted_message = (
      "В первую очередь необходимо перезагрузить сервисы в меню управления принтером"
      "Если ошибка не исчезает - просьба скинуть лог"
  )
  await message.answer(formatted_message, reply_markup=faq_kb())

@faq_router.message(F.text == 'Могу ли я модернизировать прошивку?')
async def send_can_modern(message: Message):
  formatted_message = (
      "Я не могу ответить на этот вопрос"
  )
  await message.answer(formatted_message)

@faq_router.message(F.text == 'Что делать, если возникает ошибка конфигурации?')
async def send_full_shit(message: Message):
  formatted_message = (
    "Если у вас возникает ошибка конфигурации, которую никак не исправить, то попробуйте сверить конфиг с базовой "
    "конфигурацией.Ннеобходимо подключить клавиатуру к принтеру и перейти в консольный режим (Ctrl+Alt+F3) "
    "Далее написать команду \"nano klipper/klippy/printer_base.cfg\" (Для выхода исп. Ctrl+X, для просмотра стрелки)"
  )
  await message.answer(formatted_message, reply_markup=faq_kb())

@faq_router.message(F.text == 'У меня все сломалось!')
async def send_full_shit(message: Message):
  formatted_message = (
    "Если у вас каким-либо образом все вообще сломалось, то вам может помочь "
    "программа kiauh, установленная в корневой директории $HOME "
    "Чтобы ее запустить, необходимо подключить клавиатуру к принтеру и перейти в консольный режим (Ctrl+Alt+F3) "
    "Ввести логин пароль, после ./kiauh/kiauh. Далее удалить все установленные программы и переустановить их"
    "Эта информация пригодится только тем, кто знаком с ОС linux и работе в консольном режиме"
  )
  await message.answer(formatted_message, reply_markup=faq_kb())

@faq_router.message(F.text == 'Закрыть')
async def send_full_shit(message: Message):
  kb = await main_kb(message.from_user.id)
  await message.answer("Закрываю меню частозадаваемых вопросов", reply_markup=kb)
