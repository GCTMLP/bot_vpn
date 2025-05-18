from aiogram.types import (
    CallbackQuery,
    Message,
    PreCheckoutQuery,
    LabeledPrice,
    FSInputFile
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from datetime import datetime, timedelta
import json
import logging
from logging.config import dictConfig
from connector import dp, bot

from services.depencies import (
    user_service,
    key_service,
    payment_service
)
from services.shemas import UserShema
from text.message_text import (
    HELLO,
    CHOOSE_PERIOD,
    CHOOSE_KEY,
    HELLO_TWICE,
    KEYS_LIST,
    KEY_INFO,
    PROLONG_SUCCESS_START,
    PROLONG_SUCCESS_MIDDLE,
    ADD_NEW_SUCCESS,
    MAIN_MENU,
    KEYS_LIST_EMPTY,
    HELP,
    HELP2,
    PAYMENT_EXPIRED,
    INSTRUCTION,
    BAG_MESSAGE,
    GAME_MESSAGE,
    STOP_DOING
)
from keyboards.inline_keyboards import (
    choose_period_kb,
    choose_keys_kb,
    chose_doing_markup,
    pay_markup,
    buy_key_if_empty,
    help_cancel
)
from config import (
    PRICE,
    PAYMENTS_TOKEN,
    USED_KEY_DIR,
    INSTRUCTION_DIR,
    LOGGING_CONFIG,
    ADMINS
    )

ERROR_LOG = logging.getLogger("error")
INFO_LOG = logging.getLogger("info")
dictConfig(LOGGING_CONFIG)

message_scheduler = AsyncIOScheduler()

class ProlongKey(StatesGroup):
    key = State()
    period = State()


class Help(StatesGroup):
    help_st = State()


def turn_date(date):
    y, m, d = date.split('-')
    return f'{d}.{m}.{y}'


async def admin_sender(message: Message, func_name: str):
    result_text = f"""{message.from_user.first_name}
     {message.from_user.username} trigged {func_name}"""
    for user_id in ADMINS:
        await bot.send_message(text=result_text, chat_id=user_id)

async def delete_last_bot_message(message: Message):
    try:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        ERROR_LOG.error('cant delete message')

async def remove_payment_button(message: Message):
    try:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.bot.send_message(
            text=MAIN_MENU,
            chat_id=message.chat.id,
            reply_markup=chose_doing_markup()
    )
    except:
        ERROR_LOG.error('cant remove payment button')

@dp.message(Command('start'))
async def cmd_start(message: Message):
    try:
        INFO_LOG.info(
            f'{message.from_user.first_name}'
            f' {message.from_user.username} started bot')
        user_fname = message.from_user.first_name
        user_data = UserShema(
            tg_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username)
        status = user_service().save_start_user(user_data)
        if status == 'new':
            await message.answer(
                HELLO % (user_fname),
                reply_markup=chose_doing_markup())
        elif status == 'old':
            await message.answer(
                HELLO_TWICE % (user_fname),
                reply_markup=chose_doing_markup())
        await admin_sender(message, 'cmd_start')
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in cmd_start: {str(e)}')
        await admin_sender(message, 'ERROR IN CMD')
        await message.answer(STOP_DOING)


@dp.callback_query(F.data == 'instruction')
async def send_instruction(call: CallbackQuery):
    try:
        await call.message.answer(
            INSTRUCTION,
            reply_markup=help_cancel())
        await call.message.answer_document(
            FSInputFile(INSTRUCTION_DIR+'instruction.pdf'))
        INFO_LOG.info(
            f'{call.from_user.first_name}'
            f'{call.from_user.username} get instruction')
        await delete_last_bot_message(call.message)
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in send_instruction: {str(e)}')
        await call.message.answer(STOP_DOING)


@dp.callback_query(F.data == 'help')
async def help_func(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.answer(
            HELP,
            reply_markup=help_cancel())
        await state.set_state(Help.help_st)
        INFO_LOG.info(
            f'{call.from_user.first_name} '
            f'{call.from_user.username} need help')
        await delete_last_bot_message(call.message)
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in help: {str(e)}')
        await call.message.answer(STOP_DOING)


@dp.message(Help.help_st)
async def write_help_message(message: Message, state: FSMContext):
    try:
        await message.answer(
            HELP2,
            reply_markup=help_cancel())
        for admin in ADMINS:
            await bot.send_message(
                admin,
                f'{message.from_user.username} - '
                f' {message.chat.id} написал {message.text}')
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in write_help_message: {str(e)}')


@dp.callback_query(F.data == 'cancel')
async def cancel(call: CallbackQuery, state: FSMContext):
    try:
        await state.clear()
        await call.message.answer(
            MAIN_MENU,
            reply_markup=chose_doing_markup())
        INFO_LOG.info(
            f'{call.from_user.first_name} '
            f'{call.from_user.username} click cancel')
        await delete_last_bot_message(call.message)
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in new_key: {str(e)}')


@dp.callback_query(F.data == 'new')
async def new_key(call: CallbackQuery, state: FSMContext):
    INFO_LOG.info(
        f'{call.from_user.first_name} '
        f' {call.from_user.username} whant to bye new key')
    try:
        await call.message.answer(
            CHOOSE_PERIOD,
            reply_markup=choose_period_kb())
        await state.update_data(doing='new')
        await state.set_state(ProlongKey.period)
        await delete_last_bot_message(call.message)
        await admin_sender(call, 'new_key')
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in new_key: {str(e)}')
        await admin_sender(message, 'ERROR IN new_key')
        await call.message.answer(STOP_DOING)


@dp.callback_query(F.data == 'my_keys')
async def all_key(call: CallbackQuery):
    INFO_LOG.info(
        f'{call.from_user.first_name} '
        f' {call.from_user.username} checked his keys')
    try:
        keys = key_service().get_user_keys_dates(call.from_user.id)
        markup = buy_key_if_empty()
        if not keys:
            result_message = KEYS_LIST_EMPTY
        else:
            result_message = KEYS_LIST
            for key in keys:
                result_message += KEY_INFO % (
                    key['name'],
                    turn_date(str(key['expire_at'].date())))
            markup = help_cancel()
        await call.message.answer(
            result_message,
            reply_markup=markup)
        await delete_last_bot_message(call.message)
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in all_key: {str(e)}')
        await call.message.answer(STOP_DOING)


@dp.callback_query(F.data == 'prolong')
async def prolong_key(call: CallbackQuery, state: FSMContext):
    
    try:
        keys_names = key_service().get_user_keys(call.from_user.id)
        if keys_names:
            await call.message.answer(
                CHOOSE_KEY,
                reply_markup=choose_keys_kb(keys_names))
            await state.update_data(doing='prolong')
            await state.update_data(selected=[])
            await state.set_state(ProlongKey.key)
            await state.update_data(all_keys=keys_names)
        else:
            await call.message.answer(
                KEYS_LIST_EMPTY,
                reply_markup=buy_key_if_empty())
        INFO_LOG.info(
            f'{call.from_user.first_name} '
            f'{call.from_user.username} start prolong his key')
        await delete_last_bot_message(call.message)
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in prolong_key: {str(e)}')
        await admin_sender(message, 'ERROR IN prolong_key')
        await call.message.answer(STOP_DOING)


@dp.callback_query(ProlongKey.key, F.data.contains('ovpn'))
async def chose_keys_old_key(call: CallbackQuery, state: FSMContext):
    try:
        state_data = await state.get_data()
        if 'pay' in call.data:
            selected_keys = state_data['selected']
            selected_keys_clear = [key.rstrip(' ✅') for key in selected_keys]
            await state.update_data(key=selected_keys_clear)
            await state.set_state(ProlongKey.period)
            await call.message.answer(
                CHOOSE_PERIOD,
                reply_markup=choose_period_kb())
            INFO_LOG.info(
                f'{call.from_user.first_name} '
                f'{call.from_user.username} chose key '
                f'{selected_keys_clear} to prolong')
            await delete_last_bot_message(call.message)
        else:
            key_chosen = call.data
            INFO_LOG.info(
                f'{call.from_user.first_name} '
                f'{call.from_user.username} in select key '
                f'select {key_chosen} to prolong')
            selected_keys = state_data['selected']
            if 'all' in key_chosen:
                selected_keys = key_service().get_user_keys(call.from_user.id)
            elif '✅' not in key_chosen:
                selected_keys.append(key_chosen)
            else:
                selected_keys.remove(key_chosen.rstrip(' ✅'))
            await state.update_data(selected=selected_keys)
            keys_names = state_data['all_keys']
            await bot.edit_message_text(
                text=CHOOSE_KEY,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=choose_keys_kb(keys_names, selected_keys))
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in chose_keys_old_key: {str(e)}')
        await call.message.answer(STOP_DOING)


@dp.callback_query(ProlongKey.period, F.data.startswith('mnth'))
async def pay(call: CallbackQuery, state: FSMContext):
    try:
        period = call.data.replace('mnth', '')
        state_data = await state.get_data()
        if state_data.get('doing'):
            if state_data['doing'] == 'new':
                amount = PRICE[period]*100
                description = "Покупка VPN ключа для установки"
                "VPN соединения с сервером"
            else:
                keys_names = state_data['key']
                description = f"Продление VPN ключей {' '.join(keys_names)}"
                " для установки VPN соединения с сервером",
                amount = PRICE[period]*len(keys_names)*100
            INFO_LOG.info(
                f'{call.from_user.first_name} '
                f'{call.from_user.username} chose period '
                f'{period} to prolong')
            message_pay = await bot.send_invoice(
                call.message.chat.id,
                title="Ключ VPN",
                description=description,
                provider_token=PAYMENTS_TOKEN,
                currency="RUB",
                # photo_url="",
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
                provider_data=json.dumps({
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
                                "payment_mode": "full_payment",
                                "payment_subject": "commodity"
                            }
                        ],
                        "tax_system_code": 1
                    }
                }),
                start_parameter="vpn-subscription",
                payload="test-invoice-payload",
                reply_markup=pay_markup(amount/100))
            await state.update_data(month=period)
            await admin_sender(call, 'pay')
            await delete_last_bot_message(call.message)
            INFO_LOG.info(message_pay.chat.id)
            message_scheduler.add_job(
                remove_payment_button,
                'date',
                run_date=datetime.now() + timedelta(minutes=5),
                args=[message_pay]
            )
        else:
            await call.message.answer(
                MAIN_MENU,
                reply_markup=chose_doing_markup())
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in pay: {str(e)}')
        await admin_sender(message, 'ERROR IN pay')
        await call.message.answer(STOP_DOING)


@dp.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: Message,  state: FSMContext):
    try:
        state_data = await state.get_data()
        payment_info = message.successful_payment
        INFO_LOG.info(f'''Пользователь {message.from_user.first_name} \
        {message.from_user.username} оплатил сумму \
        {str(payment_info.total_amount/100)}''')
        if state_data['doing'] == 'prolong':
            new_expire = key_service().prolong_key(
                state_data['key'],
                state_data['month'])
            result_msg = PROLONG_SUCCESS_START
            for key, expire in zip(state_data['key'], new_expire):
                result_msg += PROLONG_SUCCESS_MIDDLE % (key, expire)
            # result_msg += PROLONG_SUCCESS_END % turn_date(str(new_expire))
            await bot.send_message(
                message.chat.id,
                result_msg,
                reply_markup=chose_doing_markup())
        else:
            new_expire, filename = key_service().set_new_key(
                message.from_user.id,
                state_data['month'])
            await message.answer_document(FSInputFile(USED_KEY_DIR+filename))
            await bot.send_message(
                message.chat.id,
                ADD_NEW_SUCCESS % (
                    filename,
                    turn_date(str(new_expire))),
                reply_markup=chose_doing_markup())
        payment_service().save_payment(
            payment_info.total_amount/100,
            message.chat.id)
        await admin_sender(message, 'successful_payment')
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in successful_payment: {str(e)}')
        await message.answer(STOP_DOING)


@dp.message(Command("dice"))
async def handler_game(message: Message):
    try:
        await bot.send_dice(message.from_user.id)
        await message.answer(
            GAME_MESSAGE,
            reply_markup=help_cancel())
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in handler_game: {str(e)}')


@dp.message()
async def bad_message(message: Message):
    try:
        await message.answer(
            BAG_MESSAGE,
            reply_markup=chose_doing_markup())
        INFO_LOG.info(f'''Пользователь {message.from_user.first_name} \
        {message.from_user.username} написал {message.text}''')
        await delete_last_bot_message(message)
    except Exception as e:
        ERROR_LOG.error(f'Unknown error in bad_message: {str(e)}')
