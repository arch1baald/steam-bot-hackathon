import time
import json
from random import randint
from operator import itemgetter

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils import timezone

from .models import User, Bot, BotFriend, Message, Mailing
from .utils import (
    send_message_via_steam, update_bot_meta, accept_bot_friend_requests_and_send_welcome,
    set_bot_welcome, set_bot_response, set_bot_name, set_bot_description,
)


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
            status_code = send_message_via_steam(bot.account, bot.password, friend.steam_id, message)
            print(f'SENDING... from={bot}, to={friend}, CODE={status_code}, time={timezone.now()}')
            time.sleep(0.2)

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
    agg = dict()
    for msg in messages_queryset:
        if msg.mailing.id not in agg:
            idx = msg.mailing.id
            agg[idx] = dict()
            agg[idx]['mailing'] = idx
            agg[idx]['text'] = msg.text
            agg[idx]['sent'] = 1
        else:
            idx = msg.mailing.id
            agg[idx]['sent'] += 1

    mailings = list(agg.values())
    mailings = sorted(mailings, key=itemgetter('mailing'))
    for i, mailing in enumerate(mailings):
        mailing['number'] = i + 1
        mailing['readed'] = randint(0, mailing['sent'])
        mailing['clicked'] = int(0.75 * mailing['readed'])
        mailing['uniqueClicked'] = int(0.5 * mailing['readed'])

    mailings = sorted(mailings, key=itemgetter('number'), reverse=True)
    if len(mailings) > 3:
        # mailings = mailings[-5:]
        mailings = mailings[:3]
    return mailings


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
        bot = update_bot_meta(bot.account, bot.password, user)
    else:
        result = JsonResponse(dict(status='error', traceback='user has no bot'))
        update_headers(result)
        return result

    name = bot.name
    link = bot.steam_url
    current_friends = bot.friends_count
    max_friends = 250
    messages_queryset = Message.objects.filter(bot=bot)
    mailings = aggregate_messages(messages_queryset)
    result = JsonResponse(dict(
        nameBot=name,
        linkBot=link,
        currFriends=current_friends,
        maxFriends=max_friends,
        steamMessages=mailings,
    ))
    update_headers(result)
    return result


@require_GET
def accept_friend_requests(request):
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
    if not bots:
        result = JsonResponse(dict(status='error', traceback='user has no bot'))
        update_headers(result)
        return result

    for bot in bots:
        accept_bot_friend_requests_and_send_welcome(bot.account, bot.password, bot.welcome)

    result = JsonResponse(dict(status='ok'))
    update_headers(result)
    return result


@csrf_exempt
def set_bot_settings(request):
    """
    {
      "user": "Dmitry",
      "name": "Oleg",
      "welcome": "Poshel v Jopy",
      "description": "Daddy BOT",
      "response": "Ne pishi mne"
    }
    :param request:
    :return:
    """
    data = request.body.decode()
    if not data:
        result = JsonResponse(dict(status='empty'))
        update_headers(result)
        return result
    data = json.loads(data)

    user_name = data.get('user')
    if user_name is None:
        result = JsonResponse(dict(status='error', traceback='user is not defined'))
        update_headers(result)
        return result

    bot_welcome = data.get('welcome')
    bot_description = data.get('description')
    bot_response = data.get('response')
    bot_name = data.get('name')

    user = User.objects.filter(name=user_name)
    if user:
        user = user[0]
    else:
        result = JsonResponse(dict(status='error', traceback='user not found'))
        update_headers(result)
        return result

    bots = Bot.objects.filter(owner=user)
    if not bots:
        result = JsonResponse(dict(status='error', traceback='user has no bot'))
        update_headers(result)
        return result

    for bot in bots:
        if bot_name:
            set_bot_name(bot, bot_name)
        if bot_welcome:
            set_bot_welcome(bot, bot_welcome)
        if bot_description:
            set_bot_description(bot, bot_description)
        if bot_response:
            set_bot_response(bot, bot_response)
    result = JsonResponse(dict(status='ok'))
    update_headers(result)
    return result
