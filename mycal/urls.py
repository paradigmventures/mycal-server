from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('djadmin/', admin.site.urls),
    path('api/', include('apps.calendar.urls', namespace='calendar')),
    path('api/', include('apps.event.urls', namespace='event')),
    path('', include('apps.client.urls', namespace='client')),
]
