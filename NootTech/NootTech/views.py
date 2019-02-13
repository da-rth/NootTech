from django.views.generic import View
from django.shortcuts import render
from django.conf import settings



class IndexView(View):
    def get(self, request, *args):
        return render(request, 'index.html', {"debug": getattr(settings, "PRIVATE_DIR", None)})

class AboutView(View):
    def get(self, request, *args):
        return render(request, 'about.html')

class ToSView(View):
    def get(self, request, *args):
        return render(request, 'ToS.html')
