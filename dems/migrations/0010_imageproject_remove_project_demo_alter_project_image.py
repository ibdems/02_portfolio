# Generated by Django 5.1.1 on 2024-11-26 15:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dems", "0009_comment_project_alter_comment_blog_alter_tag_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImageProject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("image", models.ImageField(blank=True, null=True, upload_to="image/")),
            ],
        ),
        migrations.RemoveField(
            model_name="project",
            name="demo",
        ),
        migrations.AlterField(
            model_name="project",
            name="image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project_image",
                to="dems.imageproject",
            ),
        ),
    ]
