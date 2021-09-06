from django.db import models


# Create your models here.
class Hero(models.Model):
    HERO_TYPE_CHOICES = [
        ('STR', 'Strength'),
        ('AGL', 'Agility'),
        ('INT', 'Intelligence'),
    ]

    name = models.CharField(max_length=50)
    description = models.TextField()
    # i dont think it's good practice to use lambda here
    picture = models.ImageField()
    type = models.CharField(choices=HERO_TYPE_CHOICES, default='STR')
    role = models.ForeignKey('user_management.Role', on_delete=models.CASCADE)
    contr_picks = models.ForeignKey('self', on_delete=models.CASCADE)
