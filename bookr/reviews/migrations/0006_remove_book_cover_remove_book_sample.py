# Generated by Django 4.1.7 on 2023-03-13 15:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0005_book_cover_book_sample"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="cover",
        ),
        migrations.RemoveField(
            model_name="book",
            name="sample",
        ),
    ]
