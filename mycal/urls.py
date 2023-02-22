from django.contrib import admin
from django.urls import include, path

from apps.client.views import App
from apps.core.views import Route
from apps.auth.views import Login, Logout


urlpatterns = [
    path('', Route.as_view(), name='route'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('app', App.as_view(), name='app'),
    path('api/', include('apps.calendar.urls', namespace='calendar')),
    path('api/', include('apps.event.urls', namespace='event')),
    path('djadmin/', admin.site.urls),
]
