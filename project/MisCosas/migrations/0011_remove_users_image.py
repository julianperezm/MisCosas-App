# Generated by Django 3.0.3 on 2020-05-14 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MisCosas', '0010_users_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='image',
        ),
    ]
