# Generated by Django 3.1.1 on 2020-09-30 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_comment_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='index',
        ),
    ]