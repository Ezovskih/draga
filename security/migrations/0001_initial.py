# Generated by Django 5.1.6 on 2025-02-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('transport_type', models.CharField(max_length=10)),
                ('who_called', models.IntegerField()),
                ('code', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
