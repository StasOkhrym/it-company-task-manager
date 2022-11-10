# Generated by Django 4.1.3 on 2022-11-10 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager", "0003_alter_task_options_alter_task_priority"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.IntegerField(
                choices=[(1, "Urgent"), (2, "High"), (3, "Medium"), (4, "Low")],
                default=3,
            ),
        ),
    ]
