from django.views.generic import View
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .models import User
from . import serializers

# Get List of user uploads
class ListUsers(generics.ListAPIView):

    permission_classes = (AllowAny,)

    serializer_class = serializers.ListUsersSerializer

    ordering = ('-id',)

    def get_queryset(self):
        return User.objects.all()