# Generated by Django 5.0.3 on 2024-04-17 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eagle', '0006_person_password_person_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(default='default_password_value', max_length=128),
        ),
    ]
