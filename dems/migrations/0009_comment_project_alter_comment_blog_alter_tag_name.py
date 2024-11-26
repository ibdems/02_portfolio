# Generated by Django 5.1.1 on 2024-09-19 10:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dems", "0008_tache"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dems.project",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="blog",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="dems.blog"
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=100, verbose_name="tag"),
        ),
    ]
