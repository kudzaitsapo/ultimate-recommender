# Generated by Django 4.1.7 on 2023-04-05 16:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('author', models.CharField(max_length=200)),
                ('image_link', models.TextField()),
                ('genre', models.CharField(max_length=200)),
                ('rating', models.FloatField()),
                ('description', models.TextField()),
            ],
        ),
    ]