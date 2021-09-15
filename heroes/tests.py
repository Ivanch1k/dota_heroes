from django.test import TestCase, Client
from user_management.serializers import CommonUserSerializer, RoleSerializer
from user_management.models import CommonUser, Role
from heroes.serializers import ContrPickEditSerializer, HeroEditSerializer
from heroes.models import Hero, ContrPicks
from rest_framework.test import APIClient
from django.core.files import File


# Create your tests here.
class HeroTestCase(TestCase):
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
            user = serializer.create(serializer.data)
            user.is_staff = True
            user.save()
        else:
            print(serializer.errors)
        self.client = APIClient()

    def test_hero_managing(self):
        self.client.force_authenticate(user=CommonUser.objects.first())

        response = self.client.post('/api/token/', {'username': 'Test1234', 'password': '1234qwer4321'})
        self.assertEqual(response.status_code, 200)

        with open('/home/smissuser25/Pictures/Alchemist_icon.png', 'rb') as img:
            response = self.client.post('/heroes/', {
                'name': 'Alchemist',
                'description': 'Some description',
                'picture': img,
                'type': 'STR',
                'role': [1, 2, 3]
            })
            self.assertEqual(response.status_code, 201)

        with open('/home/smissuser25/Pictures/dark_alchemist.png', 'rb') as img:
            response = self.client.put('/heroes/1/', {
                'name': 'Dark Alchemist',
                'description': 'He stepped on the dark side of the force',
                'picture': img,
                'type': 'AGL',
                'role': [1, 2]
            })
            self.assertEqual(response.status_code, 200)

        response = self.client.delete('/heroes/1/')
        self.assertEqual(response.status_code, 204)

    def test_contr_picks_management(self):
        user = CommonUser.objects.first()
        user.is_staff = True
        user.save()

        self.client.force_authenticate(user=user)
        with open('/home/smissuser25/Pictures/dark_alchemist.png', 'rb') as img:
            hero_serializer = HeroEditSerializer(data=[
                {
                    'name': 'Alchemist',
                    'description': 'Simple alchemist',
                    'picture': File(img),
                    'type': 'STR',
                    'role': [1, 2, 3]
                },
                {
                    'name': 'Abaddon',
                    'description': 'Just Abaddon',
                    'picture': File(img),
                    'type': 'STR',
                    'role': [3, 4, 5]
                },
                {
                    'name': 'Ancient Apparition',
                    'description': 'Cold, cold, cold!',
                    'picture': File(img),
                    'type': 'INT',
                    'role': [4, 5]
                }
            ], many=True)

            if hero_serializer.is_valid():
                hero_serializer.create(hero_serializer.data)
            else:
                print(hero_serializer.errors)

        response = self.client.post('/heroes/contrpicks/', data={
            'hero': 2,
            'contr_picks_list': [3]
        })
        self.assertEqual(response.status_code, 201)

        response = self.client.put('/heroes/contrpicks/1/', data={
            'hero': 2,
            'contr_picks_list': [
                1, 3
            ]
        })
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/heroes/2/')
        self.assertTrue(len(response.json()['contr_picks']) == 2)

        response = self.client.delete('/heroes/contrpicks/1/')
        self.assertEqual(response.status_code, 204)
