from django.shortcuts import render
from django.http import JsonResponse


def get_config(request):
    result = {
        'key1': 'value1',
        'key2': ['list_member1', 'list_member2']
    }
    return JsonResponse(result)
