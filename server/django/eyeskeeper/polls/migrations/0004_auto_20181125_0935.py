# Generated by Django 2.1.3 on 2018-11-25 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20181125_0934'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='choice',
            table='t_polls_choice',
        ),
        migrations.AlterModelTable(
            name='question',
            table='t_polls_question',
        ),
    ]