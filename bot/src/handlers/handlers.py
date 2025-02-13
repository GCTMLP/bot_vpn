from aiogram.types import (
    CallbackQuery, 
    Message, 
    PreCheckoutQuery, 
    ContentType, 
    LabeledPrice, 
    FSInputFile
)
import os
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
import json
import logging
from connector import dp, bot
from services.depencies import user_service, key_service
from services.shemas import UserShema
from text.message_text import (
    HELLO,
    CHOOSE_PERIOD,
    CHOOSE_KEY,
    HELLO_TWICE,
    KEYS_LIST,
    KEY_INFO,
    PROLONG_SUCCESS,
    ADD_NEW_SUCCESS
)
from text.keyboard_text import (
    NEW_KEY,
    PROLONG_KEY,
    MY_KEYS
)
from keyboards.inline_keyboards import (
    choose_period_kb,
    choose_keys_kb,
    chose_doing_markup,
    pay_markup
)
from config import (
    PRICE,
    PAYMENTS_TOKEN, 
    USED_KEY_DIR,
    INSTRUCTION_DIR
    LOG
    )


class ProlongKey(StatesGroup):
    key = State()
    period = State()

@dp.message(Command('start'))
async def cmd_start(message: Message):
    try:
        LOG.info(f'{message.from_user.first_name} {message.from_user.username} started bot')
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
    except Exception as e:
        LOG.error(f'Unknown error in cmd_start: {str(e)}')

@dp.callback_query(F.data == 'instruction')
async def send_instruction(call: CallbackQuery):
    await call.message.answer_document(FSInputFile(USED_KEY_DIR+'instruction.pdf'))


@dp.callback_query(F.data == 'cancel')
async def new_key(call: CallbackQuery):
    await call.message.answer(CHOOSE_PERIOD, 
                        reply_markup=chose_doing_markup())


@dp.callback_query(F.data == 'new')
async def new_key(call: CallbackQuery, state: FSMContext):
    LOG.info(f'{call.from_user.first_name} {call.from_user.username} whant to bye new key')
    try:
        await call.message.answer(CHOOSE_PERIOD, 
                            reply_markup=choose_period_kb())
        await state.update_data(doing='new')
        await state.set_state(ProlongKey.period)
    except Exception as e:
        LOG.error(f'Unknown error in new_key: {str(e)}')


@dp.callback_query(F.data == 'my_keys')
async def all_key(call: CallbackQuery):
    LOG.info(f'{call.from_user.first_name} {call.from_user.username} checked his keys')
    try:
        markup = chose_doing_markup()
        keys = key_service().get_user_keys_dates(call.from_user.id)
        result_message = KEYS_LIST
        for key in keys:
            result_message+=KEY_INFO % (key['name'], str(key['expire_at'].date()))
        await call.message.answer(result_message, 
                            reply_markup=markup)
    except Exception as e:
        LOG.error(f'Unknown error in all_key: {str(e)}')


@dp.callback_query(F.data == 'prolong')
async def prolong_key(call: CallbackQuery, state: FSMContext):
    LOG.info(f'{call.from_user.first_name} {call.from_user.username} start prolong his key')
    try:
        keys_names = key_service().get_user_keys(call.from_user.id)
        await call.message.answer(CHOOSE_KEY, 
                            reply_markup=choose_keys_kb(keys_names))
        await state.update_data(doing='prolong')
        await state.set_state(ProlongKey.key)
    except Exception as e:
        LOG.error(f'Unknown error in prolong_key: {str(e)}')


@dp.callback_query(ProlongKey.key, F.data.endswith('ovpn'))
async def chose_period_old_key(call: CallbackQuery, state: FSMContext):
    try:
        key_chosen = call.data
        LOG.info(f'{call.from_user.first_name} {call.from_user.username} chose key {key_chosen} to prolong')
        await call.message.answer(CHOOSE_PERIOD, 
                            reply_markup=choose_period_kb())
        if 'all' in key_chosen:
            list_key_chosen = key_service().get_user_keys(call.from_user.id)
        else:
            list_key_chosen = [key_chosen]
        await state.update_data(key=list_key_chosen)
        await state.set_state(ProlongKey.period)
    except Exception as e:
        LOG.error(f'Unknown error in chose_period_old_key: {str(e)}')


@dp.callback_query(ProlongKey.period, F.data.startswith('mnth'))
async def pay_old_key(call: CallbackQuery, state: FSMContext):
    try:
        period = call.data.replace('mnth', '')
        LOG.info(f'{call.from_user.first_name} {call.from_user.username} chose period {period} to prolong')
        state_data = await state.get_data()
        if state_data['doing'] == 'new':
            amount = PRICE[period]*100
            description="Покупка VPN ключа для установки VPN соединения с сервером"
        else:
            keys_names = state_data['key']
            description=f"Продление VPN ключей {' '.join(keys_names)} для установки VPN соединения с сервером",
            amount = PRICE[period]*len(keys_names)*100
            
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
                                        amount=amount
                                    )
                                ],
                            need_email=True,
                            send_email_to_provider=True,
                            provider_data = json.dumps({
                                        "receipt": {
                                            "items": [
                                            {
                                                "description": "Ключ VPN",
                                                "quantity": "1.00",
                                                "amount": {
                                                    "value": amount/100,
                                                    "currency": "RUB"
                                                },
                                                "vat_code": 1,
                                                "payment_mode" : "full_payment",
                                                "payment_subject" : "commodity"
                                            }
                                            ],
                                            "tax_system_code" : 1
                                        }
                                        }),
                            start_parameter="vpn-subscription",
                            payload="test-invoice-payload",
                            reply_markup=pay_markup(amount/100))
        await state.update_data(month=period)
    except Exception as e:
        LOG.error(f'Unknown error in pay_old_key: {str(e)}')


@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: Message,  state: FSMContext):
    try:
        state_data = await state.get_data()
        payment_info = message.successful_payment
        LOG.info(f'''Пользователь {message.from_user.first_name} \
        {message.from_user.username} оплатил сумму {str(payment_info.total_amount/100)}''')
        if state_data['doing'] == 'prolong':
            new_expire = key_service().prolong_key(state_data['key'], state_data['month'])
            await bot.send_message(message.chat.id, 
                                PROLONG_SUCCESS %(str(payment_info.total_amount/100), 
                                                        ' '.join(state_data['key']), 
                                                        new_expire),
                                reply_markup=chose_doing_markup())
        else:
            new_expire, filename = key_service().set_new_key(message.from_user.id, state_data['month'])
            await message.answer_document(FSInputFile(USED_KEY_DIR+filename))
            await bot.send_message(message.chat.id, 
                                ADD_NEW_SUCCESS %(str(payment_info.total_amount/100), 
                                                        filename, 
                                                        new_expire.split(' ')[0]),
                                reply_markup=chose_doing_markup())
    except Exception as e:
        LOG.error(f'Unknown error in successful_payment: {str(e)}')
