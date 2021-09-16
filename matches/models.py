from django.db import models
from heroes.models import Hero

RADIANT_OR_DIRE = [
    ("R", "Radiant"),
    ("D", "Dire")
]


# Create your models here.
class Match(models.Model):
    id = models.BigAutoField(primary_key=True)
    dire_team = models.ManyToManyField(Hero, related_name='matches_as_dire')
    radiant_team = models.ManyToManyField(Hero, related_name='matches_as_radiant')
    started_datetime = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(blank=True, null=True)
    is_finished = models.BooleanField(default=False)
    winner = models.CharField(max_length=1, choices=RADIANT_OR_DIRE, blank=True, null=True)

    def __str__(self):
        return "Match #" + str(self.id)
