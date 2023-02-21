# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-01-05 04:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("resolwe_bio_kb", "0003_add_map_index"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="mapping",
            unique_together=set(
                [("source_db", "source_id", "target_db", "target_id", "relation_type")]
            ),
        ),
    ]
