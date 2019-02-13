from rest_framework import serializers
from .models import User ,ErrorVideo

class ListUsersSerializer(serializers.ModelSerializer):

	# Create new field named "is_admin" which uses "is_superuser" as source
	is_admin = serializers.CharField(source="is_superuser")

	class Meta:
		model = User
		#fields = '__all__'
		fields = ('id', 'username', 'email', 'date_joined', 'colour', 'is_admin')
#Choosing what informations to return from the APi
class errorVideoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ErrorVideo
		fields = '__all__'
		
class SettingsSerializer(serializers.ModelSerializer):
	class Meta:
		#We are storing the settings in Users so, 
		#So Model is a table in a database and the = is the FROM
		# fields is attributes of a table in a database
		model = User 
		fields = ('colour','upload_key','warnings','email')

		