import time
import json
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET


@require_GET
def get_example(request):
    result = JsonResponse({
        'key1': 'value1',
        'key2': ['list_member1', 'list_member2'],
    })
    result['Access-Control-Allow-Origin'] = '*'
    return result


@csrf_exempt
# @require_POST
def send_message_to_all_friends(request):
    endpoint = "https://steambot20181013015404.azurewebsites.net/sendall?messageText="
    response = request.body.decode()
    if not response:
        result = JsonResponse(dict(status='empty'))
        result['Access-Control-Allow-Origin'] = '*'
        return result

    response = json.loads(response)
    if 'Message' not in response or 'Id' not in response:
        result = JsonResponse(dict(status='error'))
        result['Access-Control-Allow-Origin'] = '*'
        return result

    id, message = response['Id'], response['Message']
    print(f'ID: {id}, TIME: {time.time()}, MESSAGE: {message}')
    url = f'{endpoint}{message}'
    url.replace(' ', '%20')
    requests.post(url)

    result = JsonResponse(dict(status='ok'))
    result['Access-Control-Allow-Origin'] = '*'
    return result


@require_GET
def get_settings(request):
    description = (
        'This bot demonstrates the basic functionality of the service. '
        'Next comes the useless text to check the molds on the front. '
        'Fyvaofyvshchaaofyvshchaofyvafyvalovololvrffvzgavzshgprrfshzgva'
        'prfshgrp fyscharfshrr Fyvshchrfshkvvarschf rfshvagrfshkkrfigrySUSHASHFRYVSHShR.'
    )
    welcome_message = (
        'Hello My Nigga, Let\'s make some shit: https://www.google.lt/url?sa=i'
        '&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwjK5Y3H0IPeA'
        'hVKjywKHRrrBgQQjRx6BAgBEAU&url=https%3A%2F%2Fcoub.com%2Fview%2Fzessikr&psi'
        'g=AOvVaw1_NaR_ZjqKlnfsaRMf0dMg&ust=1539527376847073'
    )
    default_response = (
        'Zbs, chotka.'
    )

    result = JsonResponse(dict(
        botName='Hackathon Steam Bot',
        botDiscription=description,
        botWelcome=welcome_message,
        botRespond=default_response,
    ))
    result['Access-Control-Allow-Origin'] = '*'
    return result


@require_GET
def get_dashboard(request):
    name = 'Hackathon Steam Bot'
    link = 'https://steamcommunity.com/id/self_motion/'
    current_friends = 15
    max_friends = 250
    text = (
        'Hello My Nigga, Let\'s make some shit: https://www.google.lt/url?sa=i'
        '&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwjK5Y3H0IPeA'
        'hVKjywKHRrrBgQQjRx6BAgBEAU&url=https%3A%2F%2Fcoub.com%2Fview%2Fzessikr&psi'
        'g=AOvVaw1_NaR_ZjqKlnfsaRMf0dMg&ust=1539527376847073'
    )
    messages = [
        dict(number=1, sent=12, readed=10, clicked=346, uniqueClicked=2134, text=text),
        dict(number=2, sent=1745, readed=0, clicked=8, uniqueClicked=444, text=text),
        dict(number=3, sent=23, readed=125, clicked=13435, uniqueClicked=5, text=text),
        dict(number=4, sent=66666, readed=54, clicked=0, uniqueClicked=0, text=text),
    ]
    result = JsonResponse(dict(
        nameBot=name,
        linkBot=link,
        currFriends=current_friends,
        maxFriends=max_friends,
        steamMessages=messages,
    ))
    result['Access-Control-Allow-Origin'] = '*'
    return result
