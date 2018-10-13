import time
import json
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def get_example(request):
    print('get_example')
    result = {
        'key1': 'value1',
        'key2': ['list_member1', 'list_member2']
    }
    return JsonResponse(result)


@csrf_exempt
@require_POST
def send_message_to_all_friends(request):
    endpoint = "https://steambot20181013015404.azurewebsites.net/sendall?messageText="
    response = json.loads(request.body.decode())
    if 'Message' not in response or 'Id' not in response:
        return

    id, message = response['Id'], response['Message']
    print(f'ID: {id}, TIME: {time.time()}, MESSAGE: {message}')
    url = f'{endpoint}{message}'
    url.replace(' ', '%20')
    print(url)
    requests.post(url)
    return JsonResponse(dict(status='ok'))
