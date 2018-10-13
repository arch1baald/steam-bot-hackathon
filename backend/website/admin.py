from django.contrib import admin

from .models import Bot, Message


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('bot', 'sent_at', 'text')
