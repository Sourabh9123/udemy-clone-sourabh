# Generated by Django 5.0.1 on 2024-03-01 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Instructor', '0007_ratingcourse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leacture',
            name='content',
            field=models.FileField(blank=True, null=True, upload_to='leacture/videos'),
        ),
    ]
