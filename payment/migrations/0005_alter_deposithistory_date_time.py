# Generated by Django 4.0.6 on 2022-07-27 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_alter_deposithistory_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposithistory',
            name='date_time',
            field=models.DateTimeField(),
        ),
    ]
