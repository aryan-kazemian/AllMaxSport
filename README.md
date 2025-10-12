# AllMaxSport

**AllMaxSport** is a Django-based e-commerce and support platform providing REST APIs for product, category, and ticket management. The project includes admin panel management, JWT authentication, filtering, searching, ordering, and comprehensive tests.

---

## Technologies & Packages Used

- **Python 3.10+**
- **Django 4.x / 5.x compatible**
- **Django REST Framework (DRF)** – for building REST APIs
- **Simple JWT** – JWT authentication for secure API access
- **SQLite** – default database (PostgreSQL or MySQL supported)
- **django-filters** – filtering support on APIs

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

## Admin Panel

- Manage **Users**, **Products**, **Categories**, **Tickets**, and **Messages**
- Ticket messages inline for easy tracking
- Product listing supports search, filter, and ordering
- Category management with dynamic creation and JSON-based features

---

## Tests

- **UserModule**: registration, login, logout, current user API
- **ProductModule**: CRUD, filtering, category handling, and permissions
- **TicketModule**: ticket creation, message management, permissions
- **Permissions**:
  - `IsStaffUser` – ensures only staff access to create/update/delete products
  - `IsOwnerOrStaff` – ensures users can manage only their tickets/messages

---

This project provides a fully functional backend for an **e-commerce platform with integrated customer support** ready for frontend integration or further customization.
