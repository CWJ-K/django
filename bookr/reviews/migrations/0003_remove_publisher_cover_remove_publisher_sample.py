# Generated by Django 4.1.7 on 2023-03-13 14:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0002_publisher_cover_publisher_sample"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="publisher",
            name="cover",
        ),
        migrations.RemoveField(
            model_name="publisher",
            name="sample",
        ),
    ]
