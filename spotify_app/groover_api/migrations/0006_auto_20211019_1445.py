# Generated by Django 3.2.8 on 2021-10-19 12:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groover_api', '0005_auto_20211018_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('album_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('album_name', models.CharField(max_length=200)),
                ('album_uri', models.TextField(blank=True, default='', null=True)),
                ('album_type', models.CharField(blank=True, default='', max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='artists',
            name='artist_followers',
        ),
        migrations.RemoveField(
            model_name='artists',
            name='artist_genres',
        ),
        migrations.RemoveField(
            model_name='artists',
            name='artist_popularity',
        ),
        migrations.RemoveField(
            model_name='artists',
            name='release_date',
        ),
        migrations.AddField(
            model_name='artists',
            name='artist_type',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='artists',
            name='artist_uri',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.CreateModel(
            name='New_Releases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_date', models.DateField(default=datetime.date(2021, 10, 19))),
                ('album_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='groover_api.album')),
                ('artist_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artists', to='groover_api.artists')),
            ],
        ),
    ]
