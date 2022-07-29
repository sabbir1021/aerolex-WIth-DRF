# Generated by Django 4.0.6 on 2022-07-27 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_alter_paymentmethod_account_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.BooleanField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('deposit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.deposit')),
            ],
        ),
    ]