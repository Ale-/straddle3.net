# Generated by Django 2.0.3 on 2018-03-22 19:37

from django.db import migrations
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='geolocation',
            field=djgeojson.fields.PointField(blank=True, verbose_name='Geolocalización'),
        ),
    ]
