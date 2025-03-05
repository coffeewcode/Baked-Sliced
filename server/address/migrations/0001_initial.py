import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('num', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=80)),
                ('street', models.CharField(max_length=80)),
                ('postal_code', models.CharField(max_length=10)),
                ('observations', models.CharField(blank=True, max_length=200)),
                ('complement', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
