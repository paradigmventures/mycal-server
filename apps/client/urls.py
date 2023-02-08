from django.urls import path

from apps.client.views import HomePage


app_name = 'client'

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
]
