# Generated by Django 3.1.1 on 2020-10-02 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
        ('vendor', '0003_auto_20201002_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='reg_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='token', to='student.student'),
        ),
    ]
