# Generated by Django 3.0.7 on 2020-09-03 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0009_auto_20200903_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inprogresshits',
            name='assignment_id',
            field=models.TextField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='inprogresshits',
            name='hit_id',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='inprogresshits',
            name='worker_id',
            field=models.TextField(),
        ),
    ]