import os.path
import re

from cloud.models import User, File
from cloud.permissions import IsStaffPermission, IsStaffOrOwnPermission, IsStaffOrOwnerPermission
from cloud.serializers import UserSerializer, AdminSerializer, FileSerializer, FileUpdateSerializer, FreefileSerializer
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from transliterate import translit


class UsersView(generics.ListAPIView, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffPermission]

    def get_queryset(self):
        return User.objects.filter(~Q(id=self.request.user.pk), is_active=True).order_by('username')

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        else:
            return super().get_permissions()

    def password_validator(self, request):
        valid_password = re.search(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}$', request.data.get('password'))

        if valid_password:
            return None
        else:
            return Response({'password': 'no'}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     validate_password(request.data.get('password'))
        #     return None
        # except ValidationError as errors:
        #     return Response({'password': list(errors)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer, **kwargs):
        serializer.save(**kwargs)

    def create(self, request, *args, **kwargs):
        response = self.password_validator(request)
        if response:
            return response
        else:
            # full_name = request.username
            password = make_password(request.data.get('password'))
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer, password=password)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffOrOwnPermission]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminSerializer
        else:
            return UserSerializer


class UserUpdateView(generics.UpdateAPIView):
    pass


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsStaffOrOwnPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileCreateView(generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsStaffOrOwnerPermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset() if request.user.is_superuser else File.objects.filter(owner=request.user.id))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['file_entity'].name = translit(serializer.validated_data['file_entity'].name,
                                                                 language_code='ru', reversed=True)
        serializer.validated_data['name'] = serializer.validated_data['file_entity'].name
        serializer.validated_data['size'] = serializer.validated_data['file_entity'].size
        serializer.validated_data['owner'] = request.user
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def get(self, request, *args, **kwargs):
    #     file_entity = self.get_object()
    #     file_path = os.path.join(settings.MEDIA_ROOT, file_entity.file_entity.name)
    #     print(file_path)
    #     if os.path.exists(file_path):
    #         file_entity.last_download = timezone.now()
    #         file_entity.save()
    #         with open(file_path, 'rb') as file:
    #             response = HttpResponse(file.read())
    #             return response
    #     else:
    #         return Response({'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)


class FileUpdateView(generics.UpdateAPIView):
    queryset = File.objects.all()
    serializer_class = FileUpdateSerializer
    permission_classes = [IsStaffOrOwnerPermission]


class FreefileView(generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = FreefileSerializer

    def get(self, request, *args, **kwargs):
        file_entity = self.get_object()
        print(file_entity)
        print(file_entity.file_entity)
        print(file_entity.file_entity.name)
        file_path = os.path.join(settings.MEDIA_ROOT, file_entity.file_entity.name)
        print(file_path)
        if file_entity.free_file:
            if os.path.exists(file_path):
                file_entity.last_download = timezone.now()
                file_entity.save()
                with open(file_path, 'rb') as file:
                    response = HttpResponse(file.read())
                    response["Content-Disposition"] = f"{'attachment'}; filename={file_entity.name}"
                    return response
            else:
                return Response({'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'nope'}, status=status.HTTP_403_FORBIDDEN)


class FileDeleteView(generics.DestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsStaffOrOwnerPermission]
