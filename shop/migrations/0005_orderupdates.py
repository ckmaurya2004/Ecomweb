# Generated by Django 4.2.2 on 2023-07-06 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUpdates',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_id', models.IntegerField(default=0)),
                ('update_desc', models.CharField(max_length=50)),
                ('timestemp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
