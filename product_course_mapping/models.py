from django.db import models
from core.models import BaseModel
from product.models import Product
from course.models import Course

class ProductCourseMapping(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='course_mappings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='product_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ('product', 'course')

    def __str__(self):
        return f"{self.product.code} -> {self.course.code}"
