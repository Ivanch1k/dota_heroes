# Generated by Django 3.2.7 on 2021-09-07 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_auto_20210907_0933'),
        ('heroes', '0008_auto_20210907_0918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hero',
            name='role',
        ),
        migrations.AddField(
            model_name='hero',
            name='role',
            field=models.ManyToManyField(related_name='heroes', to='user_management.Role'),
        ),
        migrations.CreateModel(
            name='HeroRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='heroes.hero')),
                ('roles', models.ManyToManyField(to='user_management.Role')),
            ],
        ),
    ]
