# Generated by Django 2.0.4 on 2018-05-25 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]