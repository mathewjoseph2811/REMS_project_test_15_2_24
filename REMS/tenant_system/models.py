from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TenantDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=150, blank=True, null=True)
    vchr_address = models.CharField(max_length=350, blank=True, null=True)
    json_proofs_doc = models.JSONField(blank=True, null=True)
    int_status = models.IntegerField(blank=True, null=True)
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='tenant_fk_created_details')
    dat_created = models.DateTimeField(blank=True, null=True)
    fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='tenant_fk_updated_details')
    dat_updated = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'tenant_details'