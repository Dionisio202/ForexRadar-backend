# Generated by Django 5.0.3 on 2024-04-19 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divisaData', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forexdata',
            name='frequency',
            field=models.CharField(choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')], default='D', max_length=1),
        ),
    ]
