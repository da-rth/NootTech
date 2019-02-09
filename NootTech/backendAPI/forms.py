from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from .validators import validate_email, validate_username, validate_colour
from .models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):

    #username = forms.CharField(max_length=24, validators=[validate_username])
    #email = forms.EmailField(validators=[validate_email])
    #colour = forms.CharField(max_length=7, validators=[validate_colour])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = {'username', 'email', 'colour'}


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields