# Generated by Django 3.0.2 on 2021-01-10 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Examination', '0007_auto_20210110_1246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_test_info',
            old_name='user_id',
            new_name='user',
        ),
    ]