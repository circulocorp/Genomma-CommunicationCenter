# Generated by Django 5.0.2 on 2024-02-09 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freight', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event',
            new_name='evento',
        ),
        migrations.RenameField(
            model_name='stage',
            old_name='destination',
            new_name='destino',
        ),
        migrations.RenameField(
            model_name='stage',
            old_name='origin',
            new_name='origen',
        ),
    ]