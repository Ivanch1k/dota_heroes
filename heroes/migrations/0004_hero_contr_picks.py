# Generated by Django 3.2.7 on 2021-09-07 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0003_auto_20210907_0734'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='contr_picks',
            field=models.ManyToManyField(related_name='_heroes_hero_contr_picks_+', to='heroes.Hero'),
        ),
    ]
