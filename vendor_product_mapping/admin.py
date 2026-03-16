from django.contrib import admin
from vendor_product_mapping.models import VendorProductMapping

@admin.register(VendorProductMapping)
class VendorProductMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'product', 'primary_mapping', 'is_active')
    list_filter = ('primary_mapping', 'is_active')
