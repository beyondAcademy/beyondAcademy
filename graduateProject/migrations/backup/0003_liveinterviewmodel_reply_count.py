# Generated by Django 2.2.7 on 2019-12-01 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduateProject', '0002_traderechargemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='liveinterviewmodel',
            name='reply_count',
            field=models.IntegerField(default=0),
        ),
    ]