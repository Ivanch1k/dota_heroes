from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.viewsets import ModelViewSet
import dota_heroes.settings
from user_management.models import Role, CommonUser
from user_management.serializers import RoleSerializer, CommonUserSerializer, SafeUserSerializer
from rest_framework.permissions import IsAuthenticated
from user_management.permissions import IsAdminOrReadOnly, SelfOrAdmin
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from user_management.tasks import send_simple_mail, send_email_confirmation, send_password_reset
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import QueryDict
from datetime import datetime
import hashlib


# test
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    return Response('hi:)')


# test
@api_view(['GET'])
def mail_test(request):
    send_mail(
        'Our subject',
        'Message (main text)',
        'ivan.hmyria@gmail.com',
        ['gmyrya.ivan@gmail.com'],
        fail_silently=False
    )
    return HttpResponse('Catch it :)')


# test
@api_view(['GET'])
def celery_mail_test(request):
    send_simple_mail.delay('token')
    return HttpResponse('Try to catch this one :)')


@api_view(['GET'])
def mail_confirmation_view(request):
    token = request.GET['token']
    try:
        user = CommonUser.objects.get(confirmation_token=token)
        user.is_confirmed = True
        user.is_active = True
        user.confirmation_token = ''
        user.save()
    except ObjectDoesNotExist:
        return Response('Your token is not valid', status=HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    })


# to avoid duplication. Mb should be placed elsewhere
def create_token(email):
    hash_token = hashlib.sha256()
    hash_token.update(bytes(email, 'utf-8'))
    hash_token.update(bytes(str(datetime.now()), 'utf-8'))
    hash_token.update(dota_heroes.settings.SECRET_TOKEN_KEY)
    return hash_token.hexdigest()


@api_view(['POST'])
def forgot_password(request):
    email = request.data['email']
    try:
        user = CommonUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response("User with given email doesnt exist", status=HTTP_400_BAD_REQUEST)

    token = create_token(email)
    user.password_reset_token = token
    user.save()

    send_password_reset.delay(email, token)
    return Response('Check your email.')


@api_view(['POST'])
def reset_password(request):
    new_password = request.data['new_password']
    token = request.data['token']
    try:
        user = CommonUser.objects.get(password_reset_token=token)
        # mb password validation here ??
        user.set_password(new_password)
        user.password_reset_token = ''
        user.save()
    except ObjectDoesNotExist:
        return Response('Token is not valid.', status=HTTP_400_BAD_REQUEST)
    return Response(status=HTTP_200_OK)


class RoleModelViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# mb change two viewSet by one, but try t replace some flow to not to check permissions for creating
# problem is that permission applied to entire class, but unauthorized users must have access to create method.
class UserModelViewSet(ModelViewSet):
    permission_classes = [SelfOrAdmin]
    queryset = CommonUser.objects.all()
    serializer_class = SafeUserSerializer
    http_method_names = ['get', 'put', 'delete', 'head', 'patch']

    def destroy(self, request, pk=None, *args, **kwargs):
        user = CommonUser.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return Response(status=HTTP_204_NO_CONTENT)


class RegistrationUserModelViewSet(ModelViewSet):
    serializer_class = CommonUserSerializer
    queryset = CommonUser.objects.all()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        # this block here because if we receive request, that has json in content-type header drf doesn't envelop
        # request.data in QueryDict, and as result serializer.data crashes because cant find groups and user_permissions
        # attributes. But if we receive form-data in headers then request.data will be immutable QueryDict.
        # Also if QueryDict received user created with is_active = False, and when dict - True.
        if not isinstance(request.data, QueryDict):
            request.data['groups'] = []
            request.data['user_permissions'] = []

        serializer = CommonUserSerializer(data=request.data)
        if not serializer.is_valid():
            print(type(request.data))
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        print(type(request.data))

        user = serializer.create(serializer.data)

        token = create_token(user.email)

        user.confirmation_token = token
        user.save()

        send_email_confirmation.delay(serializer.data, token)
        return Response('Please confirm your email. We send mail for you.')
