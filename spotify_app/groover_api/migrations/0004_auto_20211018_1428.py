# Generated by Django 3.2.8 on 2021-10-18 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groover_api', '0003_auto_20211018_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifytoken',
            name='access_token',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='spotifytoken',
            name='refresh_token',
            field=models.TextField(),
        ),
    ]
