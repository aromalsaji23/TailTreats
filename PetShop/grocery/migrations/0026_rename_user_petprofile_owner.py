# Generated by Django 5.1.5 on 2025-03-03 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0025_remove_petprofile_owner_petprofile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='petprofile',
            old_name='user',
            new_name='owner',
        ),
    ]
