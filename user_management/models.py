from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# photo and few common fields
def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class Role(models.Model):
    name = models.CharField('')


class CommonUser(User):
    photo = models.ImageField(upload_to=user_directory_path)
    user_role = models.OneToOneField(Role, on_delete=models.CASCADE)

