from django.test import TestCase
from user_management.serializers import CommonUserSerializer, RoleSerializer
from user_management.models import CommonUser
from rest_framework.test import APIClient


# Create your tests here.
class UserTestCase(TestCase):
    def setUp(self):
        roles_serializer = RoleSerializer(data=[
            {'name': 'Carry'},
            {'name': 'Mid-laner'},
            {'name': 'Off-lane'},
            {'name': 'Roaming Support'},
            {'name': 'Hard Support'}
        ], many=True)

        if roles_serializer.is_valid():
            roles_serializer.create(roles_serializer.data)
        else:
            print(roles_serializer.errors)

        serializer = CommonUserSerializer(data={
            'username': 'Test1234',
            'password': '1234qwer4321',
            'email': 'gmyrya.ivan@gmail.com',
            'user_roles': [1, 2],
            'groups': [],
            'user_permissions': []
        })
        if serializer.is_valid():
            serializer.create(serializer.data)
        else:
            print(serializer.errors)
        self.client = APIClient()

    def test_token_obtain(self):
        response = self.client.post('/api/token/')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/api/token/', {'username': 'Test12345', 'password': '1234qwer4321'})
        self.assertEqual(response.status_code, 401)

        response = self.client.post('/api/token/', {'username': 'Test1234', 'password': '1234qwer4321'})
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        response = self.client.post('/user/registration/', {
            'username': 'Test12345',
            'email': 'gmyrya.ivan@gmail.com',
            'user_roles': [1, 2]
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/user/registration/', {
            'username': 'Test12345',
            'password': '1234qwer4321',
            'email': 'gmyrya.ivan@gmail.com',
            'user_roles': [1, 2]
        })
        self.assertEqual(response.status_code, 200)

        self.assertTrue(CommonUser.objects.filter(username='Test12345'))

    def test_edit_profile(self):
        serializer = CommonUserSerializer(data={
            'username': 'Test_no_staff',
            'password': '1234qwer4321',
            'email': 'gmyrya.ivan@gmail.com',
            'user_roles': [1, 2],
            'groups': [],
            'user_permissions': []
        })
        if serializer.is_valid():
            serializer.create(serializer.data)
        else:
            print(serializer.errors)

        self.client.force_authenticate(user=CommonUser.objects.get(pk=2))

        with open('/home/smissuser25/Pictures/dark_alchemist.png', 'rb') as img:
            response = self.client.put('/user/1/', {
                'username': '1234',
                'email': '12345',
                'photo': img,
                'user_roles': [1, 2, 3, 4, 5]
            })
            self.assertEqual(response.status_code, 403)

        with open('/home/smissuser25/Pictures/dark_alchemist.png', 'rb') as img:
            response = self.client.put('/user/2/', {
                'username': 'Test_no_staff',
                'email': 'gmyrya.ivan@gmail.com',
                'photo': img,
                'user_roles': [1, 2, 3, 4, 5]
            })
            self.assertEqual(response.status_code, 200)

        response = self.client.post('/user/change_password/', {
            'old_password': '123123123',
            'new_password': '321321321'
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/user/change_password/', {
            'old_password': '1234qwer4321'
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/user/change_password/', {
            'old_password': '1234qwer4321',
            'new_password': '4321rewq1234'
        })
        self.assertEqual(response.status_code, 200)

        user = CommonUser.objects.get(username='Test_no_staff')
        self.assertTrue(user.check_password('4321rewq1234'))
