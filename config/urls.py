"""chat URL Configuration."""

from django.contrib import admin
from django.urls import path
from chat.front.views import chat


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chat),

]
