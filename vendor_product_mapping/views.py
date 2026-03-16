from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from vendor_product_mapping.models import VendorProductMapping
from vendor_product_mapping.serializers import VendorProductMappingSerializer

class VendorProductMappingListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="List all active vendor-product mappings",
        responses={200: VendorProductMappingSerializer(many=True)}
    )
    def get(self, request):
        mappings = VendorProductMapping.objects.filter(is_active=True)
        serializer = VendorProductMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={
            201: VendorProductMappingSerializer(),
            400: "Validation Errors"
        }
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductMappingDetailAPIView(APIView):
    def get_object(self, pk):
        from django.http import Http404
        try:
            return VendorProductMapping.objects.get(pk=pk, is_active=True)
        except VendorProductMapping.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve a vendor-product mapping",
        responses={200: VendorProductMappingSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partial update a vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={200: VendorProductMappingSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a vendor-product mapping",
        responses={204: "Deleted successfully", 404: "Not Found"}
    )
    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
