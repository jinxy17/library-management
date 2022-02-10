# Generated by Django 3.1.1 on 2020-10-30 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0007_auto_20201018_0711'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.CharField(max_length=1000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appcomments', to='Users.user')),
            ],
        ),
    ]