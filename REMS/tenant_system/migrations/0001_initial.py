# Generated by Django 4.2.10 on 2024-02-13 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TenantDetails',
            fields=[
                ('pk_bint_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('vchr_name', models.CharField(blank=True, max_length=150, null=True)),
                ('vchr_address', models.CharField(blank=True, max_length=350, null=True)),
                ('json_proofs_doc', models.JSONField(blank=True, null=True)),
                ('int_status', models.IntegerField(blank=True, null=True)),
                ('dat_created', models.DateTimeField(blank=True, null=True)),
                ('dat_updated', models.DateTimeField(blank=True, null=True)),
                ('fk_created_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tenant_fk_created', to=settings.AUTH_USER_MODEL)),
                ('fk_updated_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tenant_fk_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tenant_details',
            },
        ),
    ]