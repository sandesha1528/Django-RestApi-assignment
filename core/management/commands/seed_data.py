import random
from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping

class Command(BaseCommand):
    help = 'Seed the database with sample vendors, products, courses, certifications and mappings.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Clear existing
        Vendor.objects.all().delete()
        Product.objects.all().delete()
        Course.objects.all().delete()
        Certification.objects.all().delete()

        # Create Master Entities
        v1 = Vendor.objects.create(name='Microsoft', code='MSFT', description='Microsoft Corporation')
        v2 = Vendor.objects.create(name='Amazon Web Services', code='AWS', description='Amazon Cloud')

        p1 = Product.objects.create(name='Azure', code='AZR', description='Microsoft Azure Platform')
        p2 = Product.objects.create(name='Windows Server', code='WIN-SRV', description='Windows Server OS')
        p3 = Product.objects.create(name='AWS EC2', code='EC2', description='Elastic Compute Cloud')

        c1 = Course.objects.create(name='Azure Fundamentals', code='AZ-900', description='Basic Azure Concepts')
        c2 = Course.objects.create(name='Azure Administrator', code='AZ-104', description='Administering Azure Infrastructure')
        c3 = Course.objects.create(name='AWS Solutions Architect', code='SAA-C03', description='Architecting on AWS')

        cert1 = Certification.objects.create(name='Microsoft Certified: Azure Fundamentals', code='CERT-AZ-900', description='Entry level cert')
        cert2 = Certification.objects.create(name='Microsoft Certified: Azure Administrator Associate', code='CERT-AZ-104', description='Associate level cert')
        cert3 = Certification.objects.create(name='AWS Certified Solutions Architect - Associate', code='CERT-SAA-C03', description='Associate level cert')

        # Create Mappings
        # MSFT -> Azure (Primary) & Windows Server
        VendorProductMapping.objects.create(vendor=v1, product=p1, primary_mapping=True)
        VendorProductMapping.objects.create(vendor=v1, product=p2, primary_mapping=False)

        # AWS -> EC2
        VendorProductMapping.objects.create(vendor=v2, product=p3, primary_mapping=True)

        # Azure -> AZ-900 & AZ-104
        ProductCourseMapping.objects.create(product=p1, course=c1, primary_mapping=True)
        ProductCourseMapping.objects.create(product=p1, course=c2, primary_mapping=False)

        # EC2 -> SAA-C03
        ProductCourseMapping.objects.create(product=p3, course=c3, primary_mapping=True)

        # AZ-900 -> CERT-AZ-900
        CourseCertificationMapping.objects.create(course=c1, certification=cert1, primary_mapping=True)

        # AZ-104 -> CERT-AZ-104
        CourseCertificationMapping.objects.create(course=c2, certification=cert2, primary_mapping=True)

        # SAA-C03 -> CERT-SAA-C03
        CourseCertificationMapping.objects.create(course=c3, certification=cert3, primary_mapping=True)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with master entities and mappings!'))
