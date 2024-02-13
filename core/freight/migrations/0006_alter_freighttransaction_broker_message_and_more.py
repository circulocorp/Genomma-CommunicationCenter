# Generated by Django 5.0.2 on 2024-02-12 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freight', '0005_alter_event_options_alter_stage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freighttransaction',
            name='broker_message',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Broker message'),
        ),
        migrations.AlterField(
            model_name='freighttransaction',
            name='mzone_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Mzone code'),
        ),
        migrations.AlterField(
            model_name='freighttransaction',
            name='mzone_message',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Mzone message'),
        ),
    ]