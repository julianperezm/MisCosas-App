# Generated by Django 3.0.3 on 2020-06-04 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MisCosas', '0023_auto_20200604_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='image',
            field=models.ImageField(default='', null=True, upload_to='MisCosas'),
        ),
    ]