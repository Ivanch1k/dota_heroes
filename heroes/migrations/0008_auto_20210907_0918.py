# Generated by Django 3.2.7 on 2021-09-07 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0007_auto_20210907_0855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrpicks',
            name='contr_picks',
        ),
        migrations.AddField(
            model_name='contrpicks',
            name='contr_picks_list',
            field=models.ManyToManyField(blank=True, null=True, related_name='contr_pick_for', to='heroes.Hero'),
        ),
    ]