# Generated by Django 5.0.2 on 2024-06-24 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_cheque_etablissement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etat',
            name='date_etat',
            field=models.DateField(null=True),
        ),
    ]
