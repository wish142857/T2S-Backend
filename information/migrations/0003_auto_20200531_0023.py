# Generated by Django 3.0.6 on 2020-05-30 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('information', '0002_auto_20200531_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='receiver_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Teacher'),
        ),
    ]