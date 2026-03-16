from django.db import models
from core.models import BaseModel
from vendor.models import Vendor
from product.models import Product

class VendorProductMapping(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='product_mappings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='vendor_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ('vendor', 'product')

    def __str__(self):
        return f"{self.vendor.code} -> {self.product.code}"
