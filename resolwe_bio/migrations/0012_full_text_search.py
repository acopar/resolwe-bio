# Generated by Django 2.2.9 on 2020-01-10 16:44
import os

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.contrib.postgres.operations import TrigramExtension
from django.db import connection, migrations, models


def load_sql(apps, schema_editor):
    file_names = [
        "resolwe_indexes.sql",
    ]
    with connection.cursor() as c:
        for file_name in file_names:
            file_path = os.path.join(os.path.dirname(__file__), file_name)
            with open(file_path) as fh:
                sql_statement = fh.read()
            c.execute(sql_statement)


class Migration(migrations.Migration):

    dependencies = [
        ('resolwe_bio', '0011_nucletide_seq'),
        ('flow', '0043_full_text_search'),
    ]

    operations = [
        migrations.RunPython(load_sql),
        # Update existing entries.
        migrations.RunSQL("UPDATE flow_data SET id=id;"),
    ]
