# Generated by Django 3.0.2 on 2021-01-10 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Examination', '0006_auto_20210109_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='t_test_paper',
            old_name='question_category_id',
            new_name='question_category',
        ),
        migrations.RemoveField(
            model_name='t_question_info',
            name='question_category_id',
        ),
        migrations.RemoveField(
            model_name='t_question_info',
            name='question_type_id',
        ),
        migrations.RemoveField(
            model_name='t_question_info',
            name='test_paper_id',
        ),
        migrations.RemoveField(
            model_name='t_test_info',
            name='question_category_id',
        ),
        migrations.RemoveField(
            model_name='t_test_info',
            name='test_paper_id',
        ),
        migrations.AddField(
            model_name='t_question_info',
            name='question_category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='T_question_info_question_category_id', to='Examination.T_question_category'),
        ),
        migrations.AddField(
            model_name='t_question_info',
            name='question_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='T_question_info_question_type_id', to='Examination.T_question_type'),
        ),
        migrations.AddField(
            model_name='t_question_info',
            name='test_paper',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='T_question_info_test_paper_id', to='Examination.T_test_paper'),
        ),
        migrations.AddField(
            model_name='t_test_info',
            name='question_category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='T_test_info_question_category_id', to='Examination.T_question_category'),
        ),
        migrations.AddField(
            model_name='t_test_info',
            name='test_paper',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='T_test_info_test_paper', to='Examination.T_test_paper'),
        ),
    ]
