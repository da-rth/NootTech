from rest_framework import serializers
from .models import User, ErrorVideo


class ListUsersSerializer(serializers.ModelSerializer):
    # Create new field named "is_admin" which uses "is_superuser" as source
    # is_admin = serializers.CharField(source="is_superuser")
    class Meta:
        model = User
        #fields = '__all__'
        fields = ('id', 'username', 'email', 'date_joined', 'colour', 'is_admin')


# Choosing what informations to return from the APi
class ErrorVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorVideo
        fields = '__all__'


class SettingsSerializer(serializers.ModelSerializer):
    # These are fields we want the user to be able to POST to the backend API...
    #  allow_blank=True means the user doesn't HAVE to post this field, only the field(s) they want to update.
    gen_upload_key = serializers.BooleanField(default=False)
    email = serializers.CharField(allow_null=True)

    class Meta:
        model = User
        # On GET request, only show the below three fields of information.
        fields = ('colour', 'email', 'warnings', 'upload_key', 'gen_upload_key')



