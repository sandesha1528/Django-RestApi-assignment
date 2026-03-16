from django.db import models
from core.models import BaseModel
from course.models import Course
from certification.models import Certification

class CourseCertificationMapping(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certification_mappings')
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='course_mappings')
    primary_mapping = models.BooleanField(default=False)

    class Meta:
        unique_together = ('course', 'certification')

    def __str__(self):
        return f"{self.course.code} -> {self.certification.code}"
