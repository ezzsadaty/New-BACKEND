# Generated by Django 5.0.3 on 2024-03-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eagle', '0002_person_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(default=None, max_length=254),
            preserve_default=False,
        ),
    ]
