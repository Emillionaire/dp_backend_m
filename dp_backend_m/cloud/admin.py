from cloud.models import User, File
from django.contrib import admin


@admin.register(User)
class User(admin.ModelAdmin):
    fields = ['username', 'full_name', 'email', 'is_staff', 'password']
    list_display = ['id', 'username', 'full_name', 'email', 'is_staff', 'password', 'is_active']


@admin.register(File)
class File(admin.ModelAdmin):
    fields = ['file_entity', 'owner', 'name', 'description', 'size', 'last_download', 'free_file']
    list_display = ['id', 'file_entity', 'owner', 'name', 'description', 'size', 'created_at', 'last_download',
                    'free_file']
