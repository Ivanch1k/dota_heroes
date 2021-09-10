from django.db.models.signals import pre_save, pre_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

import dota_heroes.settings
from heroes.models import Hero
from user_management.models import CommonUser
from django.core.exceptions import ObjectDoesNotExist
import os


# mb user signals should be placed in another signals file in user_management app
# Signals for removing non-actual images
@receiver(pre_save, sender=Hero)
@receiver(pre_save, sender=CommonUser)
def hero_image_changed(sender, **kwargs):
    new_instance = kwargs['instance']
    try:
        old_instance = sender.objects.get(pk=new_instance.id)
        if sender.__name__ == 'Hero':
            if old_instance.picture != new_instance.picture:
                path = old_instance.picture.path
        elif sender.__name__ == 'CommonUser':
            if old_instance.photo != new_instance.photo:
                path = old_instance.photo.path
        os.remove(path)
    except ObjectDoesNotExist:
        print('Only new instance')
    except ValueError:
        print('No image stored')
    except UnboundLocalError:
        print('patch request')


@receiver(pre_delete, sender=Hero)
@receiver(pre_delete, sender=CommonUser)
def hero_image_deleted(sender, **kwargs):
    instance = kwargs['instance']
    try:
        if sender.__name__ == 'Hero':
            path = instance.picture.path
        elif sender.__name__ == 'CommonUser':
            path = instance.photo.path
        os.remove(path)
        os.rmdir(dota_heroes.settings.MEDIA_ROOT + '/users/user_{0}'.format(instance.id))
    except (ValueError, FileNotFoundError):
        print('No image stored')


@receiver(user_logged_in)
def test(sender, **kwargs):
    print('auth')
