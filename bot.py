import django
import os
import requests
from datetime import datetime
import telepot
import logging
import json
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Green_bot.settings")
django.setup()
from green_bot_app.models import Organisation, TelegramUser, DoorUsage
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


def get_or_create_user(msg):
    try:
        user = TelegramUser.objects.get(id_telegram=msg['from']['id'])
        return user

    except TelegramUser.DoesNotExist:
        user = TelegramUser()
        user.id_telegram = msg['from']['id']
        user.first_name = msg['from'].get('first_name')
        user.last_name = msg['from'].get('last_name')
        user.save()
        return user


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id in settings.ALOWED_CHATS:
        print('Chat:', content_type, chat_type, chat_id)
        logging.warning('Telegram raw data %s' % chat_id)

        if content_type != 'text':
            return
        command = msg['text']

        if command == f'/list@{settings.BOT_NAME}' or command == "/list":
            all_entries = Organisation.objects.order_by("order")
            parts = []
            for i, n in enumerate(all_entries, start=1):
                part = f"{i}. {n.name}"
                if n.buyer:
                    part = f"{part} (Заказывает воду)"
                parts.append(part)
            bot.sendMessage(chat_id, "\n".join(parts))

        if command == f'/open@{settings.BOT_NAME}' or command == "/open":
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Открыть', callback_data='open')]
            ])
            bot.sendMessage(chat_id, 'Открыть дверь', reply_markup=keyboard)

        if command == f'/next@{settings.BOT_NAME}' or command == "/next":
            counter = len(TelegramUser.objects.filter(voted=True))
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'Доставлена ({counter})', callback_data='yes')]
            ])
            water_buyer = Organisation.objects.get(buyer=True).name
            bot.sendMessage(chat_id, f'Доставка воды: {water_buyer}.', reply_markup=keyboard)

        if command == f'/help@{settings.BOT_NAME}' or command == "/help":
            bot.sendMessage(chat_id, 'Бот помогает упростить контроль доставки воды.'+
                                     'Имеет 2 команды: /list - перечень потребителей и /next -'+
                                     'кнопка подверждения доставки (достаточно 2-х голосов)'
                            )
    else:
        pass


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    msg_identifier = telepot.origin_identifier(msg)
    if msg['message']['chat']['id'] in settings.ALOWED_CHATS:
        print('Callback Query:', query_id, from_id, query_data)
        print('Chat_id', msg['message']['chat']['id'])
        logging.warning('Telegram raw data %s' % msg['message']['chat']['id'])
        user = get_or_create_user(msg)

        if query_data == 'yes' and user.voted is False:
            user.voted = True
            user.save()
            iteration = len(TelegramUser.objects.filter(voted=True))
            keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f'Доставлена ({iteration})', callback_data='yes')]
            ])
            bot.editMessageReplyMarkup(msg_identifier, reply_markup=keyboard1)

            if iteration >= 2:
                TelegramUser.objects.filter(voted=True).update(voted=False)
                organisation = Organisation.objects.get(buyer=True)
                organisation.buyer = False
                organisation.save()
                if len(Organisation.objects.all()) <= organisation.order:
                    organisation.order = 0
                next_order = organisation.order + 1
                next_organisation = Organisation.objects.get(order=next_order)
                next_organisation.buyer = True
                next_organisation.save()
                bot.editMessageText(msg_identifier, f'Следующий заказывает {str(next_organisation.name)}')
            bot.answerCallbackQuery(query_id, text='Голос получен')

        elif query_data == 'yes' and user.voted is True:
            bot.answerCallbackQuery(query_id, text='Вы уже подтверждали')

        elif query_data == 'open':
            door_usage = DoorUsage()
            door_usage.id_user = TelegramUser.objects.get(id_telegram=user.id_telegram)
            door_usage.request_door_time = datetime.now()
            door_usage.save()
           # last_opening = Organisation.objects.last().opened_door_time
            if user.can_open_door: #and last_opening + datetime.timedelta(seconds=settings.DOOR_SLEEP_TIME) > datetime.now():
                data = {
                    'command': 'open',
                }
                headers = {
                    'Content-type': 'application/json',
                    'Authorization': settings.DOOR_AUTH,
                }
                r = requests.post(settings.DOOR_URL, headers=headers, data=json.dumps(data))
                print(r.json())
                if r.status_code == 200:
                   # last_opening = datetime.now()
                   # last_opening.save()
                    bot.answerCallbackQuery(query_id, text='Дверь открыта')


bot = telepot.Bot(settings.BOT_TOKEN)
try:
    bot.setWebhook(settings.WEBHOOK_URL)
except telepot.exception.TooManyRequestsError:
    pass

print('Listening ...')
