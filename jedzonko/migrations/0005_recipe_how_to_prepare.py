# Generated by Django 4.0.1 on 2022-02-07 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0004_remove_recipeplan_day_name_recipeplan_day_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='how_to_prepare',
            field=models.TextField(null=True),
        ),
    ]
