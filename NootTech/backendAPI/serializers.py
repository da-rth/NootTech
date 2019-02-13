from rest_framework import serializers
from .models import User ,ErrorVideo
from .utils import get_upload_key

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
		fields = ('colour','upload_key','email')




class SettingsUpdateSerializer(serializers.ModelSerializer):
	colour = serializers.CharField()
	upload_key = serializers.BooleanField()
	email = serializers.CharField()

	class Meta:
		#We are storing the settings in Users so,
		#So Model is a table in a database and the = is the FROM
		# fields is attributes of a table in a database
		model = User
		fields = ('colour','upload_key','email')

	def create(self, instance, validated_data):
		#POST request from user to modify his own data
		# u =  All userfields that belong to the user with the request id
		u = User.objects.filter(id=self.request.user.id)
		u.colour = validated_data["colour"]
		u.email = validated_data["email"]
		#If the user requests a new upload key,
		#Function in Util will provide a randomly genenerate one
		if validated_data["upload_key"] == True:
			u.upload_key = get_upload_key()
