# Generated by Django 3.1.7 on 2021-03-21 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherReport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='cityid',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
