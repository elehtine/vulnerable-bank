# Generated by Django 4.2.5 on 2023-11-18 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='owner',
            new_name='sender',
        ),
    ]
