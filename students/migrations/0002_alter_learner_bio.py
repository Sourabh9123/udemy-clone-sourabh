# Generated by Django 5.0.1 on 2024-01-15 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
