# Generated by Django 3.2.7 on 2021-10-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Execution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rq_job_id', models.TextField(blank=True, max_length=50, null=True)),
                ('rq_job_pid', models.IntegerField(blank=True, null=True)),
                ('output_file', models.TextField(blank=True, max_length=50, null=True)),
                ('output_plain', models.TextField(blank=True, null=True)),
                ('output_error', models.TextField(blank=True, null=True)),
                ('status', models.TextField(choices=[('Requested', 'Requested'), ('Skipped', 'Skipped'), ('Running', 'Running'), ('Cancelled', 'Cancelled'), ('Error', 'Error'), ('Completed', 'Completed')], default='Requested', max_length=10)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
