# Generated by Django 4.2.13 on 2024-11-05 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "resolwe_bio_variants",
            "0008_alter_variantannotation_clinical_diagnosis_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="variant",
            name="alternative",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="variant",
            name="reference",
            field=models.TextField(),
        ),
    ]