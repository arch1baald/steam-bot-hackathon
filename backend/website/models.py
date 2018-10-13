from django.db import models


class User(models.Model):
    name = models.TextField()
    steam_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f'ID: {self.id}, steam_id: {self.steam_id}'


class Bot(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    account = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    steam_id = models.TextField(blank=True, null=True)
    friends_count = models.IntegerField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    facebook_name = models.TextField(blank=True, null=True)
    steam_url = models.URLField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    welcome = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}'


class BotFriend(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.PROTECT, default=None)
    steam_id = models.BigIntegerField()

    def __str__(self):
        # return f'ID: {self.id}, STEAM_ID: {self.steam_id}'
        return f'ID: {self.id}'


class Mailing(models.Model):
    name = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}'


class Message(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.PROTECT, default=None)
    friend = models.ForeignKey(BotFriend, on_delete=models.PROTECT, default=None)
    mailing = models.ForeignKey(Mailing, on_delete=models.PROTECT, default=None)
    text = models.TextField()
    sent_at = models.DateTimeField()

    def __str__(self):
        return f'{self.sent_at}, {self.text}'

    def to_dict(self):
        return dict(
            bot_id=self.bot.id,
            friend_id=self.friend.id,
            mailing=self.mailing.id,
            text=self.text,
            sent_at=self.sent_at,
        )
