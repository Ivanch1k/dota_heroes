# Generated by Django 3.2.7 on 2021-09-17 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0015_alter_hero_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='dota_api_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
