# Generated by Django 4.2.2 on 2023-07-10 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
