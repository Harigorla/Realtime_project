# Generated by Django 3.0 on 2020-08-09 21:04

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_recipe_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='process_val',
            field=jsonfield.fields.JSONField(default=list),
        ),
    ]
