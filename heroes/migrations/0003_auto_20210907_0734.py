# Generated by Django 3.2.7 on 2021-09-07 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0002_hero_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hero',
            name='contr_picks',
        ),
        migrations.AlterField(
            model_name='hero',
            name='picture',
            field=models.ImageField(upload_to='heroes'),
        ),
    ]
