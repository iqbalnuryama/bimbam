# Generated by Django 4.2.2 on 2023-06-25 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('murid', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='murid',
            name='tingkat',
            field=models.CharField(choices=[('Tingkat 1', 'Tingkat 1'), ('Tingkat 2', 'Tingkat 2'), ('Tingkat 3', 'Tingkat 3')], default='Tingkat 1', max_length=255),
        ),
    ]