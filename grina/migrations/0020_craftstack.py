# Generated by Django 4.1 on 2022-09-08 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grina', '0019_rename_api_link_cards_subcourse_api_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CraftStack',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('video_objects', models.ManyToManyField(to='grina.videoobject')),
            ],
        ),
    ]
