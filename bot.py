import django
import os
import time
import telepot
from green_bot_app.models import UserTelegramBot, Vote
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Green_bot.settings")
django.setup()


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        return
    command = msg['text']

    if command == '/list@GREEN_TOWN_Bot'or command == "/list":
        all_entries = UserTelegramBot.objects.order_by("order")
        parts = []
        for i, n in enumerate(all_entries, start=1):
            part = f"{i}. {n.name}"
            if n.buyer:
                part = f"{part} (Заказывает воду)"
            parts.append(part)
        bot.sendMessage(chat_id, "\n".join(parts))

    if command == '/next@GREEN_TOWN_Bot'or command == "/next":
        vote = Vote.objects.get(id=2)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Доставлена (%s )' % vote.counter, callback_data='yes'),
             InlineKeyboardButton(text='Вода отсутствует', callback_data='no')],
        ])
        bot.sendMessage(chat_id, 'Вода доставлена?', reply_markup=keyboard)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    msg_identifier = telepot.origin_identifier(msg)
    print('Callback Query:', query_id, from_id, query_data)

    if query_data == 'yes':
        vote = Vote.objects.get(id=2)
        iteration = vote.counter + 1
        Vote.objects.filter(id=2).update(counter=iteration)
        keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f'Доставлена ({iteration} )', callback_data='yes'),
             InlineKeyboardButton(text='Вода отсутствует', callback_data='no')],
        ])
        bot.editMessageReplyMarkup(msg_identifier, reply_markup=keyboard1)

        if iteration >= 3:
            Vote.objects.filter(id=2).update(counter=0)
            user = UserTelegramBot.objects.get(buyer=True)
            user.buyer = False
            user.save()
            if len(UserTelegramBot.objects.all()) <= user.order:
                user.order = 0
            next_order = user.order + 1
            next_user = UserTelegramBot.objects.get(order=next_order)
            next_user.buyer = True
            next_user.save()
            bot.editMessageText(msg_identifier, 'Следующий заказывает %s' % str(next_user.name))
    bot.answerCallbackQuery(query_id, text='Got it')


bot = telepot.Bot(settings.BOT_TOKEN)
answerer = telepot.helper.Answerer(bot)


# MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
