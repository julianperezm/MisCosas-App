# Generated by Django 3.0.3 on 2020-06-04 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MisCosas', '0021_remove_alimentador_nombreacortado'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='imagen',
            field=models.ImageField(default='', null=True, upload_to='MisCosas'),
        ),
    ]
