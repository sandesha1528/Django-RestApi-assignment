# Django REST Framework APIView Assignment

Built a modular Django backend for managing Vendors, Products, Courses, Certifications, and their mappings.

## Project Features
* Modular app design separating generic `core` functionality, `master` entities, and `mapping` entities.
* Fully utilizes raw `APIView` for all CRUD endpoints instead of Viewsets.
* Provides custom serializers performing specific tasks like checking unique constraints, duplicate mapping prevention and primary mapping singular restrictions.
* Soft-deletion implemented by disabling the `is_active` boolean field instead of hardware delete.
* Filtering support to retrieve master entities based on their relevant relationships (ex: products associated with vendor `x`).
* OpenAPI / Swagger documentation out-of-the-box leveraging `drf-yasg`.

## Setup Steps

### Prerequisites
* Python 3.8+
* Virtual Environment Configuration

### Installation
1. Clone the repository and navigate into the folder.
2. Initialize virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install django djangorestframework drf-yasg
   ```

### Database Initialization
1. Ensure you apply the existing migrations to build the tables:
   ```bash
   python manage.py migrate
   ```
2. (Optional) Create a superuser to access the Django admin dashboard:
   ```bash
   python manage.py createsuperuser
   ```

### Seed Data Module
To quickly populate the database with dummy master and mapping entity examples:
```bash
python manage.py seed_data
```

## Running the Server
Run the standard Django development server:
```bash
python manage.py runserver
```

## API Documentation
Once the server is running, the documentation is automatically generated and accessible via:
* **Swagger UI:** `http://127.0.0.1:8000/swagger/`
* **ReDoc UI:** `http://127.0.0.1:8000/redoc/`

## API Usage Examples

### Listing Products Filtered by Vendor
```http
GET /api/products/?vendor_id=1
```
*Returns all products explicitly mapped to Vendor with ID 1.*

### Creating a Parent Mapping
```http
POST /api/vendor-product-mappings/
Content-Type: application/json

{
    "vendor": 1,
    "product": 1,
    "primary_mapping": true
}
```
*Creates the mapping. Subsequent requests attempting to create a second primary mapping or an identical mapping will throw a 400 Bad Request.*

### Soft-Deleting an Entity
```http
DELETE /api/vendors/1/
```
*Will toggle the `is_active` status of the vendor record to False, excluding it from future List queries natively.*
