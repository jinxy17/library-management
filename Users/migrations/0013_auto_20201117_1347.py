# Generated by Django 3.1.1 on 2020-11-17 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0012_remove_article_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='html',
        ),
        migrations.AddField(
            model_name='article',
            name='url',
            field=models.TextField(default='https://www.baidu.com'),
        ),
    ]
