# Generated by Django 4.2.1 on 2023-08-13 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_questions_selected_useranswer_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.answers'),
        ),
    ]
