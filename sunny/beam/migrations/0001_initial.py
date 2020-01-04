# Generated by Django 3.0.2 on 2020-01-04 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('today', models.FloatField(null=True)),
                ('total', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('hour', models.IntegerField()),
                ('power', models.FloatField()),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beam.Day')),
            ],
        ),
    ]
