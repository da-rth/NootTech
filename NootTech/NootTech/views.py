from django.views.generic import View
from django.shortcuts import render
from django.conf import settings

class IndexView(View):

    def get(self, request, *args):

        context = dict()
        context["debug"] = settings.DEBUG
        context["subdomain"] = False

        subdomain = request.META['HTTP_HOST'].replace((settings.DOMAIN_NAME), "")[:-1]
        
        sharelink = '/u/' in request.build_absolute_uri()

        url = request.build_absolute_uri()

        if subdomain:
            username = url.split("//")[0].split(".")[0]
            genid = url.split("/")[-1]
            u = User.objects.get(username=username)
            f = File.objects.get(generated_filename=genid, user=u)
        
        elif sharelink:
            username = url.split("/u/")[1].split("/")[0]
            genid = url.split("/")[-1]
            u = User.objects.get(username=username)
            f = File.objects.get(generated_filename=genid, user=u)

        return render(request, 'index.html', context=context)
