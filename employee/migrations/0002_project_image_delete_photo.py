# Generated by Django 5.0.6 on 2024-06-10 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
