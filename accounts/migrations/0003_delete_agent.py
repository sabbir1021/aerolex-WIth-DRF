# Generated by Django 4.0.6 on 2022-07-25 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_agent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Agent',
        ),
    ]