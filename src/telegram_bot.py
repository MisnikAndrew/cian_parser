from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.report_utils import build_report
from utils.request_utils import get_wait_time

TOKEN = "8188415318:AAG-pRqM4vhL_o5IvGcptB-K9ZHe13Qy53Y"
max_flat_count = 500

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

class Form(StatesGroup):
    min_cost = State()
    max_cost = State()
    min_room = State()
    max_room = State()
    min_area = State()
    flat_count = State()

@dp.message_handler(commands=['start', 'report', 'help'])
async def send_welcome(msg: types.Message):
    await msg.reply(f'Привет, {msg.from_user.first_name}. Введите минимальную стоимость квартиры за месяц (например, 50000).')
    await Form.min_cost.set()

@dp.message_handler(state=Form.min_cost)
async def process_min_cost(msg: types.Message, state: FSMContext):
    try:
        min_cost = int(msg.text)
        await state.update_data(min_cost=min_cost)

        await msg.reply("Введите максимальную стоимость квартиры за месяц (например, 90000).")
        await Form.max_cost.set()
    except ValueError:
        await msg.reply("Пожалуйста, введите целое числовое значение для минимальной стоимости.")

@dp.message_handler(state=Form.max_cost)
async def process_max_cost(msg: types.Message, state: FSMContext):
    try:
        max_cost = int(msg.text)
        await state.update_data(max_cost=max_cost)

        await msg.reply("Введите минимальное кол-во комнат в квартирах (>= 1, <= 4).")
        await Form.min_room.set()
    except ValueError:
        await msg.reply("Пожалуйста, введите целое числовое значение для максимальной стоимости.")

@dp.message_handler(state=Form.min_room)
async def process_min_room(msg: types.Message, state: FSMContext):
    try:
        min_room = int(msg.text)
        await state.update_data(min_room=min_room)

        await msg.reply("Введите максимальное кол-во комнат в квартирах (>= 1, <= 4).")
        await Form.max_room.set()
    except ValueError:
        await msg.reply("Пожалуйста, введите целое числовое значение для минимального количества комнат.")

@dp.message_handler(state=Form.max_room)
async def process_max_room(msg: types.Message, state: FSMContext):
    try:
        max_room = int(msg.text)
        await state.update_data(max_room=max_room)

        await msg.reply("Введите минимальную площадь квартир (например, 30).")
        await Form.min_area.set()
    except ValueError:
        await msg.reply("Пожалуйста, введите целое числовое значение для максимального количества комнат.")

@dp.message_handler(state=Form.min_area)
async def process_min_area(msg: types.Message, state: FSMContext):
    try:
        min_area = int(msg.text)
        await state.update_data(min_area=min_area)

        await msg.reply("Введите количество квартир (например, 10). Из-за ограничений CIAN API получение большого количества квартир может быть долгим.")
        await Form.flat_count.set()
    except ValueError:
        await msg.reply("Пожалуйста, введите целое числовое значение для минимальной площади.")



@dp.message_handler(state=Form.flat_count)
async def process_flat_count(msg: types.Message, state: FSMContext):
    flat_count = int(msg.text)
    data = await state.get_data()
    min_cost = data.get('min_cost')
    max_cost = data.get('max_cost')
    min_room = data.get('min_room')
    max_room = data.get('max_room')
    min_area = data.get('min_area')
    if flat_count <= max_flat_count:
        await msg.reply(
            f'\
Минимальная стоимость: {min_cost}\n\
Максимальная стоимость: {max_cost}\n\
Минимальное количество комнат: {min_room}\n\
Максимальное количество комнат: {max_room}\n\
Минимальная площадь: {min_area}\n\
Количество квартир: {flat_count}\n\
Начинаю строить отчет, время ожидания ~{get_wait_time(flat_count)} секунд')
        try:
            report, csv_file, txt_file = build_report(min_cost, max_cost, min_room, max_room, flat_count, min_area)
            if flat_count > 3:
                await msg.reply('Отчет (только первые 3 квартиры):\n' + report)
            else:
                await msg.reply('Отчет:\n' + report)
            await msg.reply('Отчет в формате TXT:')
            await bot.send_document(msg.from_user.id, txt_file)
            await msg.reply('Отчет в формате CSV:')
            await bot.send_document(msg.from_user.id, csv_file)
            await state.finish()
        except Exception as e:
            await msg.reply(f'Произошла ошибка при создании или отправке отчета. Пожалуйста, попробуйте еще раз. Ошибка: {e}')
    else:
        await msg.reply(f'Вы ввели слишком большое количество квартир, максимальное возможное = {max_flat_count}')

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    await msg.answer(f'Вы ввели \"{msg.text.lower()}\", но я не уметь воспринимать такие сообщения. Введите /start или /report')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)