from django.contrib import admin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from .models import User, File, URL, Image, Video, Audio, Text, ReportedFile, BannedUser, ErrorVideo


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'id', 'email', 'colour']


admin.site.register(User, CustomUserAdmin)
admin.site.register(File)
admin.site.register(URL)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Audio)
admin.site.register(Text)
admin.site.register(ReportedFile)
admin.site.register(BannedUser)
admin.site.register(ErrorVideo)