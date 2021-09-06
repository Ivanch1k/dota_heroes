from django.contrib import admin
from user_management.models import CommonUser, Role


# Register your models here.
@admin.register(CommonUser)
class CommonUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

