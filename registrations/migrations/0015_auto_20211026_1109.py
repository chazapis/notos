# Generated by Django 2.2.10 on 2021-10-26 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0014_auto_20210730_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='exhibit',
            name='received',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='exhibit',
            name='start_frame',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]