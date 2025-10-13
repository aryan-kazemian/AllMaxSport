# AllMaxSport

**AllMaxSport** is a Django-based e-commerce and support platform providing REST APIs for product, category, and ticket management. The project includes admin panel management, JWT authentication, filtering, searching, ordering, and comprehensive tests.

Swagger (OpenAPI) documentation is integrated to allow easy testing and exploration of all APIs.

Docker is included for development, allowing the backend to run in a containerized environment with automatic migrations and persistent media storage.

---

## Technologies & Packages Used

- **Python 3.10+**
- **Django 4.x / 5.x compatible**
- **Django REST Framework (DRF)** – for building REST APIs
- **drf-spectacular** – OpenAPI/Swagger schema generation
- **Simple JWT** – JWT authentication for secure API access
- **SQLite** – default database (PostgreSQL or MySQL supported)
- **django-filters** – filtering support on APIs
- **Docker & Docker Compose** – containerized development environment

---

## Features

### User Module
- JWT-based authentication with access & refresh tokens
- Registration, login, logout, and current user APIs
- User profile with address and purchase info

### Product Module
- Product and category management
- Filtering, searching, and ordering APIs
- Staff/admin can create, update, and delete products
- Dynamic category creation through serializer
- Features & images stored as JSON for flexibility

### Ticket Module
- Create, update, and delete tickets with messages
- Priority and status management
- Only staff can update/delete tickets; users can manage their own messages

### Admin Panel
- Full CRUD for users, products, categories, tickets, and messages
- Inline message management for tickets
- Product listing supports search, filter, and ordering
- Simple frontend serving `index.html`  

---

## Permissions

- **Staff/Admin users**: Full access to products, categories, and tickets
- **Regular users**:
  - Read-only access to products
  - Can create tickets and manage their own messages
- **Public users**: Read-only access to product list (GET requests)

---

## API Endpoints

### User Module
- `POST /api/user/register/` – Register new user
- `POST /api/user/login/` – Login and receive JWT tokens
- `POST /api/user/logout/` – Logout (invalidate session/JWT)
- `GET /api/user/me/` – Retrieve current authenticated user

### Product Module
- `GET /api/products/` – List products (supports filtering & search)
- `POST /api/products/` – Create product (staff only)
- `PATCH /api/products/?id=<product_id>` – Update product (staff only)
- `DELETE /api/products/?id=<product_id>` – Delete product (staff only)
- `GET /api/products/?show_categories=true` – List all categories

**Filter & search query params**: `id`, `name`, `category`, `brand`, `status`, `sales`, `min_price`, `max_price`, `min_sale_price`, `max_sale_price`

### Ticket Module
- `GET /api/tickets/` – List tickets (staff sees all)
- `POST /api/tickets/` – Create ticket or add message
- `PATCH /api/tickets/?id=<ticket_id>` – Update ticket (staff only)
- `PATCH /api/tickets/?message_id=<message_id>` – Update message (owner or staff)
- `DELETE /api/tickets/?id=<ticket_id>` – Delete ticket (staff only)
- `DELETE /api/tickets/?message_id=<message_id>` – Delete message (staff only)

---

## Swagger / API Documentation

Swagger UI is available to explore all endpoints:

- **OpenAPI schema**: `/api/schema/`
- **Swagger UI**: `/api/docs/`
- **ReDoc UI**: `/api/redoc/`

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'AllMaxSport API',
    'DESCRIPTION': 'API documentation for AllMaxSport e-commerce & support platform',
    'VERSION': '1.0.0',
}
