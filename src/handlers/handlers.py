from aiogram.types import CallbackQuery, Message, PreCheckoutQuery, ContentType, LabeledPrice

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup

from connector import dp, bot
from services.depencies import user_service, key_service
from services.shemas import UserShema
from text.message_text import (
    HELLO,
    CHOOSE_PERIOD,
    CHOOSE_KEY,
    HELLO_TWICE,
    KEYS_LIST,
    KEY_INFO
)
from text.keyboard_text import (
    NEW_KEY,
    PROLONG_KEY,
    MY_KEYS
)
from keyboards.inline_keyboards import (
    choose_period_kb,
    choose_keys_kb,
    chose_doing_markup
)
from config import PRICE, PAYMENTS_TOKEN

class NewKey(StatesGroup):
    period = State()

class ProlongKey(StatesGroup):
    key = State()
    period = State()

@dp.message(Command('start'))
async def cmd_start(message: Message):
    user_fname = message.from_user.first_name
    user_data = UserShema(tg_id = message.from_user.id, first_name=message.from_user.first_name,
                        last_name = message.from_user.last_name, username=message.from_user.username)
    status = user_service().save_start_user(user_data)
    if status == 'new':
        await message.answer(HELLO % (user_fname), 
                            reply_markup=chose_doing_markup())
    elif status == 'old':
        await message.answer(HELLO_TWICE % (user_fname), 
                            reply_markup=chose_doing_markup())

@dp.callback_query(F.data == 'new')
async def new_key(call: CallbackQuery, state: FSMContext):
    await call.message.answer(CHOOSE_PERIOD, 
                        reply_markup=choose_period_kb())
    await state.update_data(doing='new')
    await state.set_state(ProlongKey.period)

@dp.callback_query(F.data == 'my_keys')
async def new_key(call: CallbackQuery):
    markup = chose_doing_markup()
    keys = key_service().get_user_keys_dates(message.from_user.id)
    result_message = KEYS_LIST
    for key in keys:
        result_message+=KEY_INFO % (key['name'], str(key['expire_at']))
    await call.message.answer(result_message, 
                        reply_markup=markup)

@dp.callback_query(F.data == 'prolong')
async def prolong_key(call: CallbackQuery, state: FSMContext):
    keys_names = key_service().get_user_keys(call.from_user.id)
    await call.message.answer(CHOOSE_KEY, 
                        reply_markup=choose_keys_kb(keys_names))
    await state.update_data(doing='prolong')
    await state.set_state(ProlongKey.key)

@dp.callback_query(ProlongKey.key, F.data.endswith('ovpn'))
async def chose_period_old_key(call: CallbackQuery, state: FSMContext):
    key_chosen = call.data
    await call.message.answer(CHOOSE_PERIOD, 
                        reply_markup=choose_period_kb())
    await state.update_data(key=key_chosen)
    await state.set_state(ProlongKey.period)

@dp.callback_query(ProlongKey.period, F.data.startswith('mnth'))
async def pay_old_key(call: CallbackQuery, state: FSMContext):
    period = call.data.replace('mnth', '')
    state_data = await state.get_data()
    if state_data['doing'] == 'new':
        description="Покупка VPN ключа для установки VPN соединения с сервером"
    else:
        description=f"Продление VPN ключа {state_data['key']} для установки VPN соединения с сервером",
    await bot.send_invoice(call.message.chat.id,
                           title="Ключ VPN",
                           description="Продление VPN ключа для установки VPN соединения с сервером",
                           provider_token=PAYMENTS_TOKEN,
                           currency="RUB",
                           #photo_url="",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[
                                LabeledPrice(
                                    label=f'На {period} месяц',
                                    amount=PRICE[period]*100
                                )
                            ],
                           start_parameter="vpn-subscription",
                           payload="test-invoice-payload")
    await state.finish()

@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message(F.content_types==ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    await bot.send_message(message.chat.id, 
                        f"Платеж на сумму {message.succes}")
