"""dotabase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^getExample/', get_example),
    url(r'^sendToFriends/', send_message_to_all_friends),
    url(r'^getSettings/', get_settings),
    url(r'^getDashboard/', get_dashboard),
    url(r'^acceptFriendRequests/', accept_friend_requests),
    url(r'^setSettings/', set_bot_settings),
]
