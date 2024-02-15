from django.contrib import admin

# Register your models here.
from .models import PropertyMaster, UnitTypes, PropertyUnitDetails

class PropertyUnitDetailsAdmin(admin.ModelAdmin):
    list_display = ('fk_property_id','get_related_field')

    def get_related_field(self, obj):
        # Assuming fk_property_id is the ForeignKey field
        property_master_id = obj.fk_property_id
        try:
            property_master = PropertyMaster.objects.get(pk=property_master_id)
            return property_master.vchr_name
        except PropertyMaster.DoesNotExist:
            return "PropertyMaster not found"

class PropertyMasterAdmin(admin.ModelAdmin):
    list_display = ('vchr_name',)

class UnitTypesAdmin(admin.ModelAdmin):
    list_display = ('vchr_name',)

admin.site.register(PropertyUnitDetails,PropertyUnitDetailsAdmin)
admin.site.register(PropertyMaster,PropertyMasterAdmin)
admin.site.register(UnitTypes,UnitTypesAdmin)

# admin.site.register(PropertyUnitDetails)
# admin.site.register(PropertyMaster)
# admin.site.register(UnitTypes)