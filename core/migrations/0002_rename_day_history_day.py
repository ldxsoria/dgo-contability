# Generated by Django 4.2.2 on 2023-06-23 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='Day',
            new_name='day',
        ),
    ]
