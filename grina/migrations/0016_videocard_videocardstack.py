# Generated by Django 4.0.4 on 2022-05-12 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grina', '0015_videoteststack'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoCard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('source', models.FileField(upload_to='grinavideos')),
                ('tip', models.CharField(max_length=200)),
                ('eng_text', models.CharField(max_length=500)),
                ('rus_text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='VideoCardStack',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('videocards', models.ManyToManyField(blank=True, to='grina.videocard')),
            ],
        ),
    ]