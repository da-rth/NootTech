from django.views.generic import View
from django.shortcuts import render
from rest_framework import generics 
from rest_framework.permissions import AllowAny
from .models import ErrorVideo ,User
from . import serializers

# Get List of user uploads
class ListUsers(generics.ListAPIView):

    permission_classes = (AllowAny,)

    serializer_class = serializers.ListUsersSerializer

    ordering = ('-id',)

    def get_queryset(self):
        return User.objects.all()


    
class errorVideoView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.errorVideoSerializer
    def get_queryset(self):
        return ErrorVideo.objects.all()