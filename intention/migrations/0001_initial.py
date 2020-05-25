# Generated by Django 3.0.6 on 2020-05-25 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruitment',
            fields=[
                ('recruitment_id', models.AutoField(primary_key=True, serialize=False)),
                ('recruitment_type', models.CharField(choices=[('UG', 'undergraduate'), ('MT', 'master'), ('DT', 'doctor')], default='UG', max_length=2)),
                ('recruitment_number', models.IntegerField()),
                ('research_fields', models.CharField(max_length=51200)),
                ('introduction', models.CharField(max_length=51200)),
                ('intention_state', models.CharField(choices=[('O', 'ongoing'), ('S', 'succeed'), ('F', 'fail')], default='O', max_length=1)),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('application_id', models.AutoField(primary_key=True, serialize=False)),
                ('research_interests', models.CharField(max_length=51200)),
                ('introduction', models.CharField(max_length=51200)),
                ('intention_state', models.CharField(choices=[('O', 'ongoing'), ('S', 'succeed'), ('F', 'fail')], default='O', max_length=1)),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Student')),
            ],
        ),
    ]
