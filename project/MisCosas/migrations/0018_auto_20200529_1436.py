# Generated by Django 3.0.3 on 2020-05-29 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MisCosas', '0017_auto_20200521_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='estadoVoto',
        ),
        migrations.RemoveField(
            model_name='users',
            name='itemsvotados',
        ),
        migrations.AlterField(
            model_name='item',
            name='enlace',
            field=models.CharField(default='yo ', max_length=64),
        ),
    ]
