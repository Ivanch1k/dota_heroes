from django.http import HttpResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.viewsets import ModelViewSet
from user_management.models import Role, CommonUser
from user_management.serializers import RoleSerializer, CommonUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST
from user_management.permissions import IsAdminOrReadOnly
from django.template import Context
from django.template.loader import get_template
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib import messages
from rest_framework.response import Response
# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    return HttpResponse('hi:)')


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


class RoleModelViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# mb change two viewSet by one, but try t replace some flow to not to check permissions for creating
class UserModelViewSet(ModelViewSet):
    # mb it would be better if user can change only himself except admin user?? (to do)
    permission_classes = [IsAuthenticated]
    queryset = CommonUser.objects.all()
    serializer_class = CommonUserSerializer
    http_method_names = ['get', 'put', 'delete', 'head', 'patch']


class RegistrationUserModelViewSet(ModelViewSet):
    serializer_class = CommonUserSerializer
    queryset = CommonUser.objects.all()
    http_method_names = ['post']
    
    # to do
    def create(self, request, *args, **kwargs):
        # validation here
        serializer = CommonUserSerializer(data=dict(request.data))
        # if not serializer.is_valid():
        #     print(serializer.errors)
        #     return Response(serializer.error_messages, status=HTTP_400_BAD_REQUEST)
        print(serializer.is_valid())
        from_email = 'ivan.hmyria@gmail.com'

        html_template = get_template('email_confirm_signup.html')
        email = serializer.data['email']
        username = serializer.data['username']
        html_content = html_template.render({'username': username})
        msg = EmailMultiAlternatives('Email confirmation', html_content, from_email, email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(request, f'Your account has been created!')
        return Response('Imagine redirect')
