from django.views.generic import View
from django.shortcuts import render

class IndexView(View):
	def get(self, request, *args):
		return render(request, 'index.html')

class AboutView(View):
	def get(self, request, *args):
		return render(request, 'about.html')

class ToSView(View):
	def get(self, request, *args):
		return render(request, 'ToS.html')