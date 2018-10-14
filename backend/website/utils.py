import urllib
import requests

from .models import User, Bot, BotFriend, Message


def send_message_via_steam(account, password, steam_id, message):
    endpoint = 'https://steambot20181013015404.azurewebsites.net/'
    method = 'sendsingle'
    message = urllib.parse.quote(str(message))
    url = f'{endpoint}{method}?user={account}&pass={password}&user64Id={steam_id}&messageText={message}'
    response = requests.post(url)
    return response.status_code


def get_bot_friend_steam_ids(account, password):
    endpoint = 'https://steambot20181013015404.azurewebsites.net/getfriendsIds/'
    url = f'{endpoint}?user={account}&pass={password}'
    response = requests.get(url)
    if response.status_code == 200:
        return list(response.json().keys())
    else:
        return None


def get_steam_id(account, password):
    endpoint = 'https://steambot20181013015404.azurewebsites.net/getbot64Id/'
    url = f'{endpoint}?user={account}&pass={password}'
    response = requests.get(url)
    if response.status_code == 200:
        return int(response.json())
    else:
        return None


def get_bot_info(account, password):
    endpoint = 'https://steambot20181013015404.azurewebsites.net/userInfo/'
    url = f'{endpoint}?user={account}&pass={password}'
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_bot_friend_info(account, password, steam_id):
    endpoint = 'https://steambot20181013015404.azurewebsites.net/friendInfo/'
    url = f'{endpoint}?user={account}&pass={password}&user64Id={steam_id}'
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def accept_bot_friend_requests_and_send_welcome(account, password, message):
    endpoint = 'https://steambot20181013015404.azurewebsites.net/acceptFriendsAndSendMessage/'
    message = urllib.parse.quote(str(message))
    url = f'{endpoint}?user={account}&pass={password}&messageText={message}'
    response = requests.post(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def update_user(name, steam_id=None):
    User.objects.update_or_create(name=name, steam_id=steam_id)


def update_bot_meta(account, password, owner):
    data = get_bot_info(account, password)
    steam_id = get_steam_id(account, password)
    Bot.objects.update_or_create(
        account=account,
        password=password,
        defaults=dict(
            owner=owner,
            name=data['botName'],
            steam_id=steam_id,
            state=data['botStatus'],
            friends_count=data['friendsCount'],
            country=data['country'],
            facebook_name=data['facebookName'],
            steam_url=data['profileUrl'],
        )
    )


def set_bot_welcome(bot, message):
    bot = Bot.objects.filter(id=bot.id)
    if bot:
        bot.update(welcome=message)


def set_bot_response(bot, message):
    bot = Bot.objects.filter(id=bot.id)
    if bot:
        bot.update(response=message)


def update_bot_friends(bot):
    data = get_bot_friend_steam_ids(bot.account, bot.password)
    for steam_id in data:
        BotFriend.objects.update_or_create(
            bot=bot,
            steam_id=steam_id,
        )
