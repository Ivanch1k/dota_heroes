from django.db.models.signals import pre_save, pre_delete, m2m_changed, post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from matches.models import Hero
from matches.models import Match


# mb user signals should be placed in another signals file in user_management app
# Signals for removing non-actual images
@receiver(m2m_changed, sender=Match.dire_team.through)
@receiver(m2m_changed, sender=Match.radiant_team.through)
def match_started(sender, **kwargs):
    if kwargs['instance'].dire_team.count() == 5 and kwargs['instance'].radiant_team.count():
        for hero in Hero.objects.all():
            hero.update_pick_rate(Match.objects.count())


@receiver(post_save, sender=Match)
def match_finished(sender, **kwargs):
    if kwargs['instance'].is_finished:
        for hero in Hero.objects.all():
            hero.update_win_rate(hero.matches_as_dire.count() + hero.matches_as_radiant.count())
