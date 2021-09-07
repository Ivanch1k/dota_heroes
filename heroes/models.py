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
    picture = models.ImageField(upload_to='heroes')
    type = models.CharField(max_length=3, choices=HERO_TYPE_CHOICES, default='STR')
    role = models.ManyToManyField('user_management.Role', related_name='heroes')

    def __str__(self):
        return self.name


# that model contains links to hero models against which our hero is weak
class ContrPicks(models.Model):
    hero = models.OneToOneField(Hero, on_delete=models.CASCADE, related_name='contr_picks')
    contr_picks_list = models.ManyToManyField(Hero, related_name='contr_pick_for', blank=True, null=True)

    def __str__(self):
        return self.hero.name
