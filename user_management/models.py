from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# photo and few common fields
def user_directory_path(instance, filename):
    return "users/user_{0}/{1}".format(instance.id, filename)


class Role(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class CommonUser(User):
    photo = models.ImageField(upload_to=user_directory_path)
    # user_role = models.OneToOneField(Role, on_delete=models.CASCADE)
    user_roles = models.ManyToManyField(Role, related_name='users')
