import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils import timezone

import pandas as pd

from .models import User, Bot, BotFriend, Message, Mailing
from .utils import send_message_via_steam, update_bot_meta


def update_headers(result):
    result["Access-Control-Allow-Origin"] = "*"
    result["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
    result["Access-Control-Max-Age"] = "1000"
    result["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"


@csrf_exempt
def send_message_to_all_friends(request):
    data = request.body.decode()
    if not data:
        result = JsonResponse(dict(status='empty'))
        update_headers(result)
        return result

    data = json.loads(data)
    if 'Message' not in data or 'user' not in data:
        result = JsonResponse(dict(status='error', traceback='Message or user is not defined'))
        update_headers(result)
        return result

    user_name, message = data.get('user'), data['Message']
    mailing_name = data.get('mailing')
    if user_name is None:
        result = JsonResponse(dict(status='error', traceback='user is not defined'))
        update_headers(result)
        return result

    user = User.objects.filter(name=user_name)
    if user:
        user = user[0]
    else:
        result = JsonResponse(dict(status='error', traceback='user not found'))
        update_headers(result)
        return result

    bots = Bot.objects.filter(owner=user)
    if bots:
        mailing = Mailing.objects.create(name=mailing_name)
    for bot in bots:
        bot_friends = BotFriend.objects.filter(bot=bot)
        for friend in bot_friends:
            Message.objects.create(
                bot=bot,
                friend=friend,
                mailing=mailing,
                text=message,
                sent_at=timezone.now(),
            )
            print(f'SENDING... from={bot}, to={friend}, time={timezone.now()}')
            send_message_via_steam(bot.account, bot.password, friend.steam_id, message)

    result = JsonResponse(dict(status='ok'))
    update_headers(result)
    return result


@require_GET
def get_example(request):
    result = JsonResponse({
        'key1': 'value1',
        'key2': ['list_member1', 'list_member2'],
    })
    update_headers(result)
    return result


@require_GET
def get_settings(request):
    user_name = request.GET.get('user', None)
    if user_name is None:
        result = JsonResponse(dict(status='error', traceback='user is not defined'))
        update_headers(result)
        return result

    user = User.objects.filter(name=user_name)
    if user:
        user = user[0]
    else:
        result = JsonResponse(dict(status='error', traceback='user not found'))
        update_headers(result)
        return result

    bots = Bot.objects.filter(owner=user)
    if bots:
        bot = bots[0]
    else:
        result = JsonResponse(dict(status='error', traceback='user has no bot'))
        update_headers(result)
        return result

    result = JsonResponse(dict(
        botName=bot.name,
        botDiscription=bot.description,
        botWelcome=bot.welcome,
        botRespond=bot.response,
    ))
    update_headers(result)
    return result


def aggregate_messages(messages_queryset):
    df_messages = pd.DataFrame([msg.to_dict() for msg in messages_queryset])
    #TODO: id, sent, text


@require_GET
def get_dashboard(request):
    user_name = request.GET.get('user', None)
    if user_name is None:
        result = JsonResponse(dict(status='error', traceback='user is not defined'))
        update_headers(result)
        return result

    user = User.objects.filter(name=user_name)
    if user:
        user = user[0]
    else:
        result = JsonResponse(dict(status='error', traceback='user not found'))
        update_headers(result)
        return result

    bots = Bot.objects.filter(owner=user)
    if bots:
        bot = bots[0]
    else:
        result = JsonResponse(dict(status='error', traceback='user has no bot'))
        update_headers(result)
        return result

    # update_bot_meta(bot.account, bot.password, user)

    name = bot.name
    link = bot.steam_url
    current_friends = bot.friends_count
    max_friends = 250
    messages_queryset = Message.objects.filter(bot=bot)

    text = 'asdgasdg'
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
    update_headers(result)
    return result
