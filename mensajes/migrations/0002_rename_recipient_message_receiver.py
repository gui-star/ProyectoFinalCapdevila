# Generated by Django 4.2.2 on 2023-07-10 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mensajes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='recipient',
            new_name='receiver',
        ),
    ]
