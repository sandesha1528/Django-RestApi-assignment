from rest_framework import serializers
from vendor_product_mapping.models import VendorProductMapping

class VendorProductMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProductMapping
        fields = ['id', 'vendor', 'product', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        vendor = data.get('vendor')
        product = data.get('product')
        primary_mapping = data.get('primary_mapping', False)

        if not self.instance:
            if VendorProductMapping.objects.filter(vendor=vendor, product=product).exists():
                raise serializers.ValidationError("This vendor to product mapping already exists.")

        # Ensure single primary mapping per parent (vendor)
        if primary_mapping:
            vendor_obj = vendor or (self.instance.vendor if self.instance else None)
            existing_primary = VendorProductMapping.objects.filter(vendor=vendor_obj, primary_mapping=True)
            if self.instance:
                existing_primary = existing_primary.exclude(id=self.instance.id)

            if existing_primary.exists():
                raise serializers.ValidationError("This vendor already has a primary product mapping.")

        return data
