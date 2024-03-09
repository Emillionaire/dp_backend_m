from cloud.models import User, File
from rest_framework import serializers


class AdminSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'email', 'is_staff']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class FileSerializer(serializers.ModelSerializer):
    file_entity = serializers.FileField(write_only=True)
    size = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = File
        fields = ['id', 'file_entity', 'owner', 'name', 'description', 'size', 'created_at', 'last_download', 'free_file', 'url']


class FileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['pk', 'description', 'free_file']


class FreefileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file_entity', 'owner', 'name', 'description', 'size', 'created_at', 'last_download', 'free_file']
