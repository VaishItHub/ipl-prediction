# Generated by Django 5.1.4 on 2024-12-13 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0007_delete_players'),
    ]

    operations = [
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
                ('player_name', models.CharField(max_length=100)),
                ('strike_rate', models.FloatField(max_length=10)),
                ('role', models.CharField(max_length=100)),
            ],
        ),
    ]
