from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from vendor.models import Vendor
from vendor.serializers import VendorSerializer

class VendorListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="List all active vendors",
        responses={200: VendorSerializer(many=True)}
    )
    def get(self, request):
        vendors = Vendor.objects.filter(is_active=True)
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new vendor",
        request_body=VendorSerializer,
        responses={
            201: VendorSerializer(),
            400: "Validation Errors"
        }
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailAPIView(APIView):
    def get_object(self, pk):
        from django.http import Http404
        try:
            return Vendor.objects.get(pk=pk, is_active=True)
        except Vendor.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve a vendor",
        responses={200: VendorSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a vendor (Full)",
        request_body=VendorSerializer,
        responses={200: VendorSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def put(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partial update a vendor",
        request_body=VendorSerializer,
        responses={200: VendorSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def patch(self, request, pk):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a vendor",
        responses={204: "Deleted successfully", 404: "Not Found"}
    )
    def delete(self, request, pk):
        vendor = self.get_object(pk)
        vendor.is_active = False
        vendor.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
