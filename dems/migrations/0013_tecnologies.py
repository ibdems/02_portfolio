# Generated by Django 5.1.1 on 2024-12-02 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dems", "0012_remove_project_image_imageproject_project_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tecnologies",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "project",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to="dems.project"
                    ),
                ),
            ],
        ),
    ]