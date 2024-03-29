# Generated by Django 3.0.6 on 2020-06-19 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Information',
            fields=[
                ('information_id', models.AutoField(primary_key=True, serialize=False)),
                ('receiver_type', models.CharField(choices=[('T', 'teacher'), ('S', 'student')], max_length=1)),
                ('information_type', models.CharField(choices=[('T', 'txt'), ('P', 'picture')], default='T', max_length=1)),
                ('information_state', models.CharField(choices=[('N', 'new'), ('R', 'read'), ('H', 'hide')], default='N', max_length=1)),
                ('information_content', models.BinaryField()),
                ('information_time', models.DateTimeField(auto_now_add=True)),
                ('receiver_student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Student')),
                ('receiver_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Teacher')),
            ],
        ),
    ]
