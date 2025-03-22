# Generated by Django 5.1.7 on 2025-03-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userModule_App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('INR', 'INR')], max_length=3),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'M'), ('F', 'F')], max_length=10),
        ),
    ]
