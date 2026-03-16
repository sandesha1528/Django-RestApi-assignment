from django.contrib import admin
from course_certification_mapping.models import CourseCertificationMapping

@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'certification', 'primary_mapping', 'is_active')
    list_filter = ('primary_mapping', 'is_active')
