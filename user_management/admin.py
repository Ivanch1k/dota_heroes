from django.contrib import admin
from user_management.models import CommonUser, Role


# Register your models here.
@admin.register(CommonUser, Role)
class UserAdmin(admin.ModelAdmin):
    pass
