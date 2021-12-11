# Generated by Django 3.2.9 on 2021-12-10 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_alter_comment_recomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='ReComment',
        ),
        migrations.AddField(
            model_name='recomment',
            name='comment',
            field=models.OneToOneField(default=-1, on_delete=django.db.models.deletion.CASCADE, to='app1.comment', verbose_name='回复ID'),
        ),
    ]
