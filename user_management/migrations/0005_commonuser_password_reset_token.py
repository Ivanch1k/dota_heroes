# Generated by Django 3.2.7 on 2021-09-08 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_auto_20210908_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonuser',
            name='password_reset_token',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
