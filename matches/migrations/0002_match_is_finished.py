# Generated by Django 3.2.7 on 2021-09-16 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
    ]
