# Generated by Django 2.2.5 on 2019-11-12 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0004_participant_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Federation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=32)),
                ('country_code', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterField(
            model_name='traveldetails',
            name='ticket_price',
            field=models.CharField(blank=True, help_text='If to be paid by the Organising Committee', max_length=64),
        ),
    ]
