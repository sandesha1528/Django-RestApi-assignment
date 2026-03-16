from rest_framework import serializers
from product_course_mapping.models import ProductCourseMapping

class ProductCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCourseMapping
        fields = ['id', 'product', 'course', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        product = data.get('product')
        course = data.get('course')
        primary_mapping = data.get('primary_mapping', False)

        if not self.instance:
            if ProductCourseMapping.objects.filter(product=product, course=course).exists():
                raise serializers.ValidationError("This product to course mapping already exists.")

        if primary_mapping:
            product_obj = product or (self.instance.product if self.instance else None)
            existing_primary = ProductCourseMapping.objects.filter(product=product_obj, primary_mapping=True)
            if self.instance:
                existing_primary = existing_primary.exclude(id=self.instance.id)

            if existing_primary.exists():
                raise serializers.ValidationError("This product already has a primary course mapping.")

        return data
