from bot import on_callback_query, on_chat_message, bot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import telepot
import json
import logging


@csrf_exempt
def pass_update(request):
    raw = request.body.decode('utf8')
    logging.debug('Telegram raw data %s', raw)
    update = json.loads(raw)

    if 'message' in update:
        data = message = update['message']
    elif 'callback_query' in update:
        data = update['callback_query']
    else:
        return HttpResponse('OK')
    
    try:
        flavor = telepot.flavor(data)
        if flavor == 'chat':
            on_chat_message(data)
        elif flavor == 'callback_query':
            on_callback_query(data)
        else:
            return HttpResponse('OK')
    except Exception as e:
        logging.exception('Error on handling bot message')
    
    return HttpResponse('OK')
