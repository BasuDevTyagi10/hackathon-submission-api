# Generated by Django 4.2.1 on 2023-05-03 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='submission_link',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submission_file',
            field=models.FileField(null=True, upload_to='hackathon_submissions/'),
        ),
    ]