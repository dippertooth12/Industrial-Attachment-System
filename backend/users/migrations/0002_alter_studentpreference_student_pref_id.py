# Generated by Django 5.1.7 on 2025-04-07 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentpreference',
            name='student_pref_id',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
