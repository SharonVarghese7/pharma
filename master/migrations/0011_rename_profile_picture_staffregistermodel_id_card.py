# Generated by Django 4.0 on 2021-12-14 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0010_staffregistermodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staffregistermodel',
            old_name='Profile_picture',
            new_name='id_card',
        ),
    ]