# Generated by Django 4.1.7 on 2023-03-09 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sudoku', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='difficulty',
            old_name='Difficulty',
            new_name='Option',
        ),
        migrations.AddField(
            model_name='difficulty',
            name='FieldsToRemove',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
