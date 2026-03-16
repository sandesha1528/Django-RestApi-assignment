from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from certification.models import Certification
from certification.serializers import CertificationSerializer

class CertificationListCreateAPIView(APIView):
    course_id_param = openapi.Parameter(
        'course_id', openapi.IN_QUERY, 
        description="Filter certifications by course ID", 
        type=openapi.TYPE_INTEGER
    )

    @swagger_auto_schema(
        operation_description="List all active certifications, with optional course filter",
        manual_parameters=[course_id_param],
        responses={200: CertificationSerializer(many=True)}
    )
    def get(self, request):
        queryset = Certification.objects.filter(is_active=True)
        course_id = request.query_params.get('course_id')
        if course_id:
            from course_certification_mapping.models import CourseCertificationMapping
            mapped_cert_ids = CourseCertificationMapping.objects.filter(
                course_id=course_id, is_active=True
            ).values_list('certification_id', flat=True)
            queryset = queryset.filter(id__in=mapped_cert_ids)

        serializer = CertificationSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new certification",
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer(), 400: "Validation Errors"}
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificationDetailAPIView(APIView):
    def get_object(self, pk):
        from django.http import Http404
        try:
            return Certification.objects.get(pk=pk, is_active=True)
        except Certification.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_description="Retrieve a certification",
        responses={200: CertificationSerializer(), 404: "Not Found"}
    )
    def get(self, request, pk):
        cert = self.get_object(pk)
        serializer = CertificationSerializer(cert)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a certification (Full)",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def put(self, request, pk):
        cert = self.get_object(pk)
        serializer = CertificationSerializer(cert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partial update a certification",
        request_body=CertificationSerializer,
        responses={200: CertificationSerializer(), 400: "Validation Errors", 404: "Not Found"}
    )
    def patch(self, request, pk):
        cert = self.get_object(pk)
        serializer = CertificationSerializer(cert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Soft delete a certification",
        responses={204: "Deleted successfully", 404: "Not Found"}
    )
    def delete(self, request, pk):
        cert = self.get_object(pk)
        cert.is_active = False
        cert.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
