# Generated by Django 4.2.1 on 2023-08-16 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_useranswer_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='correct',
            field=models.CharField(max_length=50),
        ),
    ]
