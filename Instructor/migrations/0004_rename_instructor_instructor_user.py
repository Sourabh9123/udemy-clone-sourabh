# Generated by Django 5.0.1 on 2024-01-15 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Instructor', '0003_alter_instructor_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instructor',
            old_name='instructor',
            new_name='user',
        ),
    ]