from django.db import models


class Bot(models.Model):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    welcome = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'ID: {self.id}, Name: {self.name}'


class Message(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.PROTECT)
    text = models.TextField()
    sent_at = models.DateTimeField()

    def __str__(self):
        return f'{self.sent_at}, {self.text}'
