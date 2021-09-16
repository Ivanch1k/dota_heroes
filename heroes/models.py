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

    pick_rate = models.FloatField(default=0)
    win_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def update_pick_rate(self, total):
        matches_as_dire = self.matches_as_dire.count()
        matches_as_radiant = self.matches_as_radiant.count()
        self.pick_rate = (matches_as_radiant + matches_as_dire) / total
        self.save()

    def update_win_rate(self, total):
        win_as_dire = self.matches_as_dire.filter(winner="D").count()
        win_as_radiant = self.matches_as_radiant.filter(winner="R").count()
        self.win_rate = (win_as_radiant + win_as_dire) / total
        self.save()


# that model contains links to hero models against which our hero is weak
# !model name shouldn't be plural!
class ContrPicks(models.Model):
    hero = models.OneToOneField(Hero, on_delete=models.CASCADE, related_name='contr_picks')
    contr_picks_list = models.ManyToManyField(Hero, related_name='contr_pick_for', blank=True, null=True)

    def __str__(self):
        return self.hero.name
