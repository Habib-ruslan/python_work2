import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot = Bot(token="5961065774:AAEaX_pOb44CuuBagT8RQrWypJkBfsNuKtc")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class RegistrationForm(StatesGroup):
    name = State()
    race_type = State()


@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Привет! Для записи на марафон введи своё ФИО.")
    await RegistrationForm.name.set()  # Устанавливаем состояние name


@dp.message_handler(state=RegistrationForm.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)  # Сохраняем ФИО в состоянии
    await message.reply("Выбери тип забега.", reply_markup=get_race_types_keyboard())
    await RegistrationForm.next()  # Переходим к следующему состоянию race_type


@dp.message_handler(state=RegistrationForm.race_type)
async def process_race_type(message: types.Message, state: FSMContext):
    race_type = message.text
    await state.update_data(race_type=race_type)
    data = await state.get_data()
    await message.reply(f"Спасибо! Ты записан на марафон.\n\n"
                        f"ФИО: {data['name']}\n"
                        f"Тип забега: {data['race_type']}")
    await state.finish()


def get_race_types_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Полумарафон (21 км)"))
    keyboard.add(KeyboardButton("Марафон (42 км)"))
    keyboard.add(KeyboardButton("Сверхмарафон(100 км)"))
    return keyboard


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dp.start_polling())
    loop.close()
