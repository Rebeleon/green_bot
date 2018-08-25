from bot import webhook
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def pass_update(request):
    webhook.feed(request.body)
    return HttpResponse('DONE')
