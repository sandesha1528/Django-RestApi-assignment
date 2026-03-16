from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from course_certification_mapping.models import CourseCertificationMapping
from course_certification_mapping.serializers import CourseCertificationMappingSerializer

class CourseCertificationMappingListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="List all active course-certification mappings",
        responses={200: CourseCertificationMappingSerializer(many=True)}
    )
    def get(self, request):
        mappings = CourseCertificationMapping.objects.filter(is_active=True)
        serializer = CourseCertificationMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer(), 400: "Validation Errors"}
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseCertificationMappingDetailAPIView(APIView):
    def get_object(self, pk):
        from django.http import Http404
        try:
            return CourseCertificationMapping.objects.get(pk=pk, is_active=True)
        except CourseCertificationMapping.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve a course-certification mapping",
        responses={200: CourseCertificationMappingSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partial update a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={200: CourseCertificationMappingSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a course-certification mapping",
        responses={204: "Deleted successfully", 404: "Not Found"}
    )
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
