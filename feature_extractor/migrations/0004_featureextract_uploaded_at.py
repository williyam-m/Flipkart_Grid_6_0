# Generated by Django 5.1.1 on 2024-10-17 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feature_extractor', '0003_featureextract_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='featureextract',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
