# Generated by Django 3.2.5 on 2022-04-11 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20220412_0304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredienthistory',
            options={'ordering': ['date_purchased']},
        ),
        migrations.AlterField(
            model_name='ingredienthistory',
            name='type',
            field=models.CharField(choices=[('purchase', 'PURCHASE'), ('consume', 'CONSUME')], default='purchase', max_length=20),
        ),
    ]