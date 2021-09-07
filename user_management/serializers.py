from rest_framework.serializers import ModelSerializer
from user_management.models import Role, CommonUser


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class CommonUserSerializer(ModelSerializer):
    class Meta:
        model = CommonUser
        fields = '__all__'
