# Generated by Django 2.1.3 on 2018-12-23 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training_data', '0002_trainingdata_number_of_entries'),
        ('sine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingdata',
            name='training_data',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='training_data.TrainingData'),
            preserve_default=False,
        ),
    ]
