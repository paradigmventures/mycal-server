from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View


class Route(View):

    def get(self, request):
        if request.user.is_authenticated:
            redirect_url = reverse('app')
        else:
            redirect_url = reverse('login')
        return HttpResponseRedirect(redirect_url)
