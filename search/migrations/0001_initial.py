# Generated by Django 3.0.6 on 2020-06-19 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchRecord',
            fields=[
                ('search_record_id', models.AutoField(primary_key=True, serialize=False)),
                ('search_key', models.CharField(max_length=64)),
                ('search_time', models.DateTimeField()),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
