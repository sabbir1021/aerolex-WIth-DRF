# Generated by Django 4.0.6 on 2022-07-26 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0002_agent_agent_type_alter_agent_country_and_more'),
        ('accounts', '0009_user_agent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent.agent'),
        ),
    ]
