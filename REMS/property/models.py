from django.db import models
from tenant_system.models import TenantDetails
from django.contrib.auth.models import User
# Create your models here.
class PropertyMaster(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=150, blank=True, null=True)
    vchr_address = models.CharField(max_length=350, blank=True, null=True)
    vchr_location = models.CharField(max_length=350, blank=True, null=True)
    txt_features = models.TextField( blank=True, null=True)
    int_status = models.IntegerField(blank=True, null=True)
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='property_fk_created')
    dat_created = models.DateTimeField(blank=True, null=True)
    fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='property_fk_updated')
    dat_updated = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'property_master'
        
        
class UnitTypes(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    vchr_name = models.CharField(max_length=150, blank=True, null=True)
    vchr_code = models.CharField(max_length=150, blank=True, null=True)
    int_status = models.IntegerField(blank=True, null=True)

    
    class Meta:

        db_table = 'unit_types'


class PropertyUnitDetails(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_property = models.ForeignKey(PropertyMaster, models.DO_NOTHING, blank=True, null=True,related_name='property_master_id')
    dbl_rent = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fk_unit_types = models.ForeignKey(UnitTypes, models.DO_NOTHING, blank=True, null=True,related_name='unit_types_selected_id')
    fk_tenant = models.ForeignKey(TenantDetails, models.DO_NOTHING, blank=True, null=True,related_name='tenant_selected_id')
    int_status = models.IntegerField(blank=True, null=True)
    dat_agreement_end = models.DateField(blank=True, null=True)
    dat_rent_payout = models.DateField(blank=True, null=True)
    fk_created = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='property_units_fk_created')
    dat_created = models.DateTimeField(blank=True, null=True)
    fk_updated = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True,related_name='property_units_fk_updated')
    dat_updated = models.DateTimeField(blank=True, null=True)

    class Meta:

        db_table = 'property_unit_details'