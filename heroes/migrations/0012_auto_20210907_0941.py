# Generated by Django 3.2.7 on 2021-09-07 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0011_auto_20210907_0937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hero',
            name='contr_picks',
        ),
        migrations.AddField(
            model_name='contrpicks',
            name='contr_picks_list',
            field=models.ManyToManyField(blank=True, null=True, related_name='contr_pick_for', to='heroes.Hero'),
        ),
        migrations.AddField(
            model_name='contrpicks',
            name='hero',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contr_picks', to='heroes.hero'),
        ),
        migrations.DeleteModel(
            name='HeroRole',
        ),
    ]
