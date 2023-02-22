from django.views.generic import TemplateView


class App(TemplateView):
    template_name = "index.html"
