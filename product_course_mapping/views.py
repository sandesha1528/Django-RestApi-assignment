from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from product_course_mapping.models import ProductCourseMapping
from product_course_mapping.serializers import ProductCourseMappingSerializer

class ProductCourseMappingListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="List all active product-course mappings",
        responses={200: ProductCourseMappingSerializer(many=True)}
    )
    def get(self, request):
        mappings = ProductCourseMapping.objects.filter(is_active=True)
        serializer = ProductCourseMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer(), 400: "Validation Errors"}
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCourseMappingDetailAPIView(APIView):
    def get_object(self, pk):
        from django.http import Http404
        try:
            return ProductCourseMapping.objects.get(pk=pk, is_active=True)
        except ProductCourseMapping.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve a product-course mapping",
        responses={200: ProductCourseMappingSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partial update a product-course mapping",
        request_body=ProductCourseMappingSerializer,
        responses={200: ProductCourseMappingSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a product-course mapping",
        responses={204: "Deleted successfully", 404: "Not Found"}
    )
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
