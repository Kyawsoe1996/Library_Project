# Generated by Django 3.1.4 on 2021-07-09 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0021_borrowbook_return_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='avail_qty',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]