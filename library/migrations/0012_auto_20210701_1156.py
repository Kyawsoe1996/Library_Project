# Generated by Django 3.1.4 on 2021-07-01 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_borrow_borrowbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='borrow_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
