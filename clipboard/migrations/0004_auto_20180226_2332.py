# Generated by Django 2.0 on 2018-02-26 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clipboard', '0003_filemetaentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filemetaentry',
            name='file_entry_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='clipboard.Entry'),
        ),
    ]