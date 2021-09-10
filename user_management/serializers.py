from rest_framework.serializers import ModelSerializer
from user_management.models import Role, CommonUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class SafeUserSerializer(ModelSerializer):
    class Meta:
        model = CommonUser
        exclude = ('password', 'confirmation_token', 'password_reset_token', )
        read_only_fields = ('last_login', 'id', 'is_superuser', 'is_staff', 'is_confirmed',
                            'is_active', 'date_joined', 'user_permissions', 'groups')


class CommonUserSerializer(ModelSerializer):
    class Meta:
        model = CommonUser
        fields = '__all__'

    def create(self, validated_data):
        new_user = ModelSerializer.create(self, validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user
