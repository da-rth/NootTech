from django.contrib import admin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
from .models import User, File, Image, Video, Audio, Text, ReportedFile, BannedUser, ErrorVideo, FavouritedFile, VirusTotalScan

"""
Configure the admin panel to order information.
"""

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['id', 'username', 'email', 'colour', 'upload_key', 'is_active']

class VirusAdmin(admin.ModelAdmin):
    list_display = ('id', 'File', 'user')
    def File(self, obj):
        return obj.file_pointer
    
    def user(self, obj):
        return obj.file_pointer.user

    user.username = 'username'
    user.admin_order_field = '__username'
    
    File.original_filename = 'original_filename'
    File.admin_order_field = '__original_filenme'

class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_filename', 'generated_filename', 'ip', 'is_private', 'views', 'user')
    def user(self, obj):
        return obj.user
    user.username = 'username'
    user.admin_order_field = '__username'

class FavouritedAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'File', 'user')

    def File(self, obj):
        return obj.file

    def user(self, obj):
        return obj.user
    user.username = 'username'
    user.admin_order_field = '__username'

    File.original_filename = 'original_filename'
    File.admin_order_field = '__original_filenme'

class ReportAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'File', 'reason_title', 'by_user', 'user', 'date')

    def File(self, obj):
        return obj.reported_file

    def by_user(self, obj):
        return obj.reported_by
    
    def user(self, obj):
        return obj.reported_file.user

    user.username = 'username'
    user.admin_order_field = '__username'

    by_user.username = 'username'
    by_user.admin_order_field = '__username'

    File.original_filename = 'original_filename'
    File.admin_order_field = '__original_filenme'

class BanAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'user', 'banned_by', 'date')

    def user(self, obj):
        return obj.banned_user

    def banned_by(self, obj):
        return obj.banned_by

    user.username = 'username'
    user.admin_order_field = '__username'
    
    banned_by.username = 'username'
    banned_by.admin_order_field = '__username'

admin.site.register(User, CustomUserAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(VirusTotalScan, VirusAdmin)
admin.site.register(FavouritedFile, FavouritedAdmin)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Audio)
admin.site.register(Text)
admin.site.register(ReportedFile, ReportAdmin)
admin.site.register(BannedUser, BanAdmin)
admin.site.register(ErrorVideo)