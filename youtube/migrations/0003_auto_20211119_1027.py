# Generated by Django 3.1.3 on 2021-11-19 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youtube', '0002_auto_20211119_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='publishedAt',
            field=models.DateTimeField(),
        ),
    ]
