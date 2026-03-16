from django.contrib import admin
from product_course_mapping.models import ProductCourseMapping

@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'course', 'primary_mapping', 'is_active')
    list_filter = ('primary_mapping', 'is_active')
