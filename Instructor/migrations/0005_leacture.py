# Generated by Django 5.0.1 on 2024-01-16 07:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Instructor', '0004_rename_instructor_instructor_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('order', models.PositiveIntegerField()),
                ('content', models.FileField(blank=True, null=True, upload_to=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leactures', to='Instructor.course')),
            ],
        ),
    ]
