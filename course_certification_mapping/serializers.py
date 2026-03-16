from rest_framework import serializers
from course_certification_mapping.models import CourseCertificationMapping

class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCertificationMapping
        fields = ['id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        course = data.get('course')
        certification = data.get('certification')
        primary_mapping = data.get('primary_mapping', False)

        if not self.instance:
            if CourseCertificationMapping.objects.filter(course=course, certification=certification).exists():
                raise serializers.ValidationError("This course to certification mapping already exists.")

        if primary_mapping:
            course_obj = course or (self.instance.course if self.instance else None)
            existing_primary = CourseCertificationMapping.objects.filter(course=course_obj, primary_mapping=True)
            if self.instance:
                existing_primary = existing_primary.exclude(id=self.instance.id)

            if existing_primary.exists():
                raise serializers.ValidationError("This course already has a primary certification mapping.")

        return data
