import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Green_bot.settings")
django.setup()
import time
import json
import threading
import random
import telepot
from green_bot_app.models import UserTelegramBot, Vote
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from django.conf import settings

"""
$ python3.5 skeleton_route.py <token>
It demonstrates:
- passing a routing table to `MessageLoop` to filter flavors.
- the use of custom keyboard and inline keyboard, and their various buttons.
Remember to `/setinline` and `/setinlinefeedback` to enable inline mode for your bot.
It works like this:
- First, you send it one of these 4 characters - `c`, `i`, `h`, `f` - and it replies accordingly:
    - `c` - a custom keyboard with various buttons
    - `i` - an inline keyboard with various buttons
    - `h` - hide custom keyboard
    - `f` - force reply
- Press various buttons to see their effects
- Within inline mode, what you get back depends on the **last character** of the query:
    - `a` - a list of articles
    - `p` - a list of photos
    - `b` - to see a button above the inline results to switch back to a private chat with the bot
"""

message_with_inline_keyboard = None


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        return
    callback_data = msg.get('data')
    command = msg['text']

    if command == '/list@GREEN_TOWN_Bot'or command == "/list":
        all_entries = UserTelegramBot.objects.order_by("order")
        '''
        message = ''
        i = 1
        for n in all_entries:
            if n.buyer == "Заказ":
                n = str(n) + " (Заказывает воду)"
            n = str(i) + ". " + str(n)
            i += 1
            message += (str(n) + "\n")
        bot.sendMessage(chat_id, message)
        '''
        parts = []
        for i, n in enumerate(all_entries, start=1):
            part = f"{i}. {n.name}"
            if n.buyer:
                part = f"{part} (Заказывает воду)"
            parts.append(part)
        bot.sendMessage(chat_id, "\n".join(parts))

    if command == '/next@GREEN_TOWN_Bot'or command == "/next":
        vote = Vote.objects.get(id=2)
        print(msg['message_id'])
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Доставлена (%s )' % vote.counter, callback_data='yes'),
             InlineKeyboardButton(text='Вода отсутствует', callback_data='no')],
        ])
        bot.sendMessage(chat_id, 'Вода доставлена?', reply_markup=keyboard)
        #if not vote.message_id:
        vote.message_id = telepot.message_identifier
        vote.save()


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    if query_data == 'yes':
        vote = Vote.objects.get(id=2)
        iteration = vote.counter + 1
        Vote.objects.filter(id=2).update(counter=iteration)
        keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Доставлена (%s )' % iteration, callback_data='yes'),
             InlineKeyboardButton(text='Вода отсутствует', callback_data='no')],
        ])
        # editor = telepot.helper.Editor(bot, msg_ident)
        bot.editMessageReplyMarkup(vote.message_id, reply_markup=keyboard1)

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
            bot.editMessageText(count.message_id, 'Следующий заказывает %s' % str(next_user.name))
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
