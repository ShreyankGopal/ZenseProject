# Generated by Django 4.2.1 on 2023-08-27 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_quiz_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='TimeLimit',
        ),
    ]
