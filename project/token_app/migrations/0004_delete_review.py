# Generated by Django 4.1.7 on 2023-04-03 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('token_app', '0003_review'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]