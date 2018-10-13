from django.contrib import admin

from .models import Bot, Message, BotFriend, User


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot', 'sent_at', 'text')


@admin.register(BotFriend)
class BotFriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'bot', 'steam_id')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'steam_id')
