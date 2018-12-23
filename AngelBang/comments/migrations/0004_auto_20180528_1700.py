# Generated by Django 2.0.4 on 2018-05-28 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('comments', '0003_auto_20180525_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='email',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='name',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='post',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='url',
        ),
        migrations.AddField(
            model_name='comments',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comments',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comments',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
