# Generated by Django 3.1.1 on 2020-09-30 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='index',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]