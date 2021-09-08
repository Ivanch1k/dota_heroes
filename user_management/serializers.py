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

    def create(self, validated_data):
        new_user = ModelSerializer.create(self, validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user
