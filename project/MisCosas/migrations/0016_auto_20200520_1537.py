# Generated by Django 3.0.3 on 2020-05-20 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MisCosas', '0015_auto_20200520_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='image',
            field=models.ImageField(default='', upload_to='MisCosas'),
        ),
    ]
