import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('store_pickup', 'Store Pickup'), ('delivery', 'Delivery')], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('estimated_time', models.CharField(max_length=30)),
                ('observations', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.address')),
            ],
        ),
    ]
