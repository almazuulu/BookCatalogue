# Generated by Django 4.2.5 on 2023-10-03 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='name',
            new_name='author_name',
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='name',
            new_name='genre_name',
        ),
    ]
