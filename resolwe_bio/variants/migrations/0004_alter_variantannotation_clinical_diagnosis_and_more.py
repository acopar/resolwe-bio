# Generated by Django 4.2.13 on 2024-09-12 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "resolwe_bio_variants",
            "0003_remove_variantannotationtranscript_transcript_ids_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="variantannotation",
            name="clinical_diagnosis",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="variantannotationtranscript",
            name="annotation",
            field=models.CharField(max_length=500),
        ),
    ]