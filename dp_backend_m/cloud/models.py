import os.path

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


def storage_path_generator(instance, filename):
    return os.path.join(instance.owner.username, filename)


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, validators=[MinLengthValidator(3)])
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, error_messages={'unique': 'This email already used.'})
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return f'username: {self.username}, full_name: {self.full_name}, email: {self.email}'


class File(models.Model):
    file_entity = models.FileField(upload_to=storage_path_generator)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, default='')
    size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(blank=True, null=True)
    free_file = models.BooleanField(blank=True, default=False)

