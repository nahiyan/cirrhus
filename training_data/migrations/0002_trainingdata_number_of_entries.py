# Generated by Django 2.1.3 on 2018-12-23 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingdata',
            name='number_of_entries',
            field=models.IntegerField(default=0),
        ),
    ]
