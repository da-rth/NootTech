from rest_framework import serializers
from .models import User ,ErrorVideo

class ListUsersSerializer(serializers.ModelSerializer):

	# Create new field named "is_admin" which uses "is_superuser" as source
	is_admin = serializers.CharField(source="is_superuser")

	class Meta:
		model = User
		#fields = '__all__'
		fields = ('id', 'username', 'email', 'date_joined', 'colour', 'is_admin')

class errorVideoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ErrorVideo
		fields = '__all__'
		
	