from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from course.models import Course
from course.serializers import CourseSerializer

class CourseListCreateAPIView(APIView):
    product_id_param = openapi.Parameter(
        'product_id', openapi.IN_QUERY, 
        description="Filter courses by product ID", 
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(
        operation_description="List all active courses, with optional product filter",
        manual_parameters=[product_id_param],
        responses={200: CourseSerializer(many=True)}
    )
    def get(self, request):
        queryset = Course.objects.filter(is_active=True)
        product_id = request.query_params.get('product_id')
        if product_id:
            from product_course_mapping.models import ProductCourseMapping
            mapped_course_ids = ProductCourseMapping.objects.filter(
                product_id=product_id, is_active=True
            ).values_list('course_id', flat=True)
            queryset = queryset.filter(id__in=mapped_course_ids)

        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new course",
        request_body=CourseSerializer,
        responses={201: CourseSerializer(), 400: "Validation Errors"}
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailAPIView(APIView):
    def get_object(self, pk):
        from django.http import Http404
        try:
            return Course.objects.get(pk=pk, is_active=True)
        except Course.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve a course",
        responses={200: CourseSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a course (Full)",
        request_body=CourseSerializer,
        responses={200: CourseSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partial update a course",
        request_body=CourseSerializer,
        responses={200: CourseSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def patch(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a course",
        responses={204: "Deleted successfully", 404: "Not Found"}
    )
    def delete(self, request, pk):
        course = self.get_object(pk)
        course.is_active = False
        course.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
