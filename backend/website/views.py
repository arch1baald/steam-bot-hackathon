import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils import timezone

from .models import User, Bot, BotFriend, Message
from .utils import send_message_via_steam


def update_headers(result):
    result["Access-Control-Allow-Origin"] = "*"
    result["Access-Control-Allow-Methods"] = "GET, OPTIONS, POST"
    result["Access-Control-Max-Age"] = "1000"
    result["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"


@csrf_exempt
# TODO: user_name via request
def send_message_to_all_friends(request, user_name='Dmitry'):
    data = request.body.decode()
    if not data:
        result = JsonResponse(dict(status='empty'))
        update_headers(result)
        return result

    data = json.loads(data)
    if 'Message' not in data:
        result = JsonResponse(dict(status='error'))
        update_headers(result)
        return result

    message = data['Message']

    user = User.objects.filter(name=user_name)
    # TODO: unique checks via steam_id
    user = user[0]
    bots = Bot.objects.filter(owner=user)
    for bot in bots:
        bot_friends = BotFriend.objects.filter(bot=bot)
        for friend in bot_friends:
            print(f'SENDING... from={bot}, to={friend}, time={timezone.now()}')
            Message.objects.create(
                bot=bot,
                friend=friend,
                text=message,
                sent_at=timezone.now(),
            )
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
def get_settings(request, user_name='Dmitry'):
    user = User.objects.filter(name=user_name)
    # TODO: unique checks via steam_id
    user = user[0]
    bots = Bot.objects.filter(owner=user)
    if bots:
        bot = bots[0]
    else:
        result = JsonResponse(dict(status='error'))
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
    update_headers(result)
    return result
