# Generated by Django 2.0.4 on 2018-05-30 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_auto_20180530_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='root_comment', to='comments.Comments'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent_comment', to='comments.Comments'),
        ),
    ]
