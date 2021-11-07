# Generated by Django 2.2.10 on 2021-10-26 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0015_auto_20211026_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibit',
            name='exhibit_class',
            field=models.CharField(choices=[('A1', 'A1. Court of Honour'), ('A2', 'A2. Official Class'), ('A3', 'A3. Jury Class'), ('A4', 'A4. Other exhibits'), ('B1', 'B1. Classe des Champions'), ('C1', 'C1. Traditional Philately'), ('C2', 'C2. Postal History'), ('C3', 'C3. Postal Stationery'), ('C4', 'C4. Aerophilately'), ('C5', 'C5. Astrophilately'), ('C6', 'C6. Revenues'), ('C7', 'C7. Thematic Philately'), ('C8', 'C8. Maximaphily'), ('C9', 'C9. Open Philately'), ('C10', 'C10. Picture Postcards'), ('Y1', 'Y1. Youth Philately - Exhibitor’s age (at 1.1.2021) 10-15 years'), ('Y2', 'Y2. Youth Philately - Exhibitor’s age (at 1.1.2021) 16-18 years'), ('Y3', 'Y3. Youth Philately - Exhibitor’s age (at 1.1.2021) 19-21 years'), ('L1', 'L1. Philatelic Literature – Books of research nature, specialised catalogues'), ('L2', 'L2. Philatelic Literature – Books of promotional and documentary character'), ('L3', 'L3. Philatelic Literature – General catalogues'), ('L4', 'L4. Philatelic Literature – Periodicals'), ('L5', 'L5. Philatelic Literature – Articles (collections of)'), ('L6', 'L6. Philatelic Literature – Websites'), ('L7', 'L7. Philatelic Literature – Software'), ('L8', 'L8. Philatelic Literature – Other digital works')], max_length=4),
        ),
    ]