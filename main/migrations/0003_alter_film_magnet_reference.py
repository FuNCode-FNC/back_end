# Generated by Django 4.0.6 on 2022-07-10 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_scheduledforviewing_episode_ref_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='magnet_reference',
            field=models.CharField(max_length=300, verbose_name='magnet link'),
        ),
    ]
