# Generated by Django 4.1.3 on 2022-12-03 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mavuno', '0002_product_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='phone',
            field=models.CharField(db_index=True, default=707741793, max_length=200),
            preserve_default=False,
        ),
    ]
