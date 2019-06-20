"""pysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views as main_views
from guestbook import views as guestbook_views
from user import views as user_views

urlpatterns = [
    path('guestbook/delete', guestbook_views.delete),
    path('guestbook/deleteform/<int:id>', guestbook_views.deleteform),
    path('guestbook/add', guestbook_views.add),
    path('user/joinsuccess', user_views.joinsuccess),
    path('user/join', user_views.join),
    path('user/joinform', user_views.joinform),
    path('guestbook/', guestbook_views.list),
    path('', main_views.index),
    path('admin/', admin.site.urls),
]
