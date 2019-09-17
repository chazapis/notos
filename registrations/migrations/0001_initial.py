# Generated by Django 2.2.5 on 2019-09-17 07:45

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exhibit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('short_description', models.TextField()),
                ('exhibit_class', models.CharField(choices=[('B1', 'B1. Classe des Champions'), ('C1', 'C1. Traditional Philately'), ('C2', 'C2. Postal History'), ('C3', 'C3. Postal Stationery'), ('C4', 'C4. Aerophilately'), ('C5', 'C5. Astrophilately'), ('C6', 'C6. Revenues'), ('C7', 'C7. Thematic Philately'), ('C8', 'C8. Maximaphily'), ('C9', 'C9. Open Philately'), ('C10', 'C10. Picture Postcards'), ('L1', 'L1. Philatelic Literature – Books of research nature, specialised catalogues'), ('L2', 'L2. Philatelic Literature – Books of promotional and documentary character'), ('L3', 'L3. Philatelic Literature – General catalogues'), ('L4', 'L4. Philatelic Literature – Periodicals'), ('L5', 'L5. Philatelic Literature – Articles (collections of)'), ('L6', 'L6. Philatelic Literature – Websites'), ('L7', 'L7. Philatelic Literature – Software'), ('L8', 'L8. Philatelic Literature – Other digital works'), ('Y1', 'Y1. Youth Philately - Exhibitor’s age (at 1.1.2021) 10-15 years'), ('Y2', 'Y2. Youth Philately - Exhibitor’s age (at 1.1.2021) 16-18 years'), ('Y3', 'Y3. Youth Philately - Exhibitor’s age (at 1.1.2021) 19-21 years')], max_length=4)),
                ('date_of_birth', models.DateField(blank=True, help_text='Youth phiilately only', null=True)),
                ('frames', models.IntegerField(choices=[(1, 1), (2, 2), (4, 4), (6, 6), (8, 8)])),
                ('remarks', models.TextField(blank=True)),
                ('author', models.CharField(blank=True, max_length=256)),
                ('publisher', models.CharField(blank=True, max_length=128)),
                ('year_of_publication', models.IntegerField(blank=True, null=True)),
                ('pages', models.IntegerField(blank=True, null=True)),
                ('format', models.CharField(blank=True, max_length=64)),
                ('frequency', models.CharField(blank=True, max_length=64)),
                ('availability', models.CharField(blank=True, max_length=64)),
                ('price', models.CharField(blank=True, max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('changed_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('MR', 'Mr'), ('MRS', 'Mrs'), ('MISS', 'Miss'), ('DR', 'Dr')], default='MR', max_length=4)),
                ('surname', models.CharField(max_length=128)),
                ('name', models.CharField(help_text='Include any middle names', max_length=128)),
                ('address', models.TextField()),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('commissioner_country', django_countries.fields.CountryField(blank=True, help_text='State here if you are a national commissioner for another country', max_length=2)),
                ('telephone', models.CharField(blank=True, max_length=32)),
                ('mobile', models.CharField(max_length=32)),
                ('language', models.CharField(choices=[('EN', 'English'), ('EL', 'Greek')], default='EN', help_text='Communication language', max_length=2)),
                ('remarks', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('changed_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExhibitParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exhibition_level', models.CharField(choices=[('WORLD', 'FIP World'), ('CONT', 'FEPA/FIAF/FIAP Continental'), ('INT', 'Other International'), ('NAT', 'National')], max_length=8)),
                ('exhibition_name', models.CharField(max_length=128)),
                ('points', models.IntegerField()),
                ('medal', models.CharField(blank=True, choices=[('LG', 'Large Gold'), ('G', 'Gold'), ('LV', 'Large Vermeil'), ('V', 'Vermeil'), ('LS', 'Large Silver'), ('S', 'Silver'), ('SB', 'Silver Bronze'), ('B', 'Bronze')], max_length=2)),
                ('special_prize', models.BooleanField()),
                ('felicitations', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('changed_at', models.DateTimeField(auto_now=True)),
                ('exhibit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participations', to='registrations.Exhibit')),
            ],
        ),
        migrations.AddField(
            model_name='exhibit',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrations.Participant'),
        ),
    ]