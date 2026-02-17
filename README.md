# Backend Developer Intern – Technical Assignment: Role-Based Blog API

## Overview
This project implements a Role-Based Blog API with authentication and authorization, as per the provided technical assignment requirements. The API uses JWT for authentication and enforces role-based access control (RBAC) for three roles: ADMIN (full CRUD access to all blogs), AUTHOR (CRUD on own blogs), and READER (view only published blogs).

## Tech Stack

- Django
- Django REST Framework (DRF)
- PostgreSQL
- JWT Authentication (via djangorestframework-simplejwt)

## Project Structure

```
blog/
├── blog_api/          # Project settings and URLs
├── accounts/             # Custom user model, serializers, management command
├── blogs/             # Blog model, views, serializers, permissions
├── migrations/        # Provided migration files (in users/ and blogs/)
├── manage.py
├── requirements.txt   # Dependencies
└── README.md
```

### 1. Custom User Model

- Created using AbstractBaseUser (alternative: AbstractUser could be used).
- Added role field with choices: ADMIN, AUTHOR, READER.
- Implemented a custom user manager (CustomUserManager) for create_user and create_superuser, handling email as the primary field and password hashing.
- Used @property for role-based logic: is_admin, is_author, is_reader.

### 2. Authentication

- Implemented JWT Authentication with token obtain/refresh endpoints.
- Protected APIs using DRF permissions and custom logic.
- Only authenticated users can access protected routes (e.g., create/update/delete); unauthenticated can view published blogs if applicable.

### 3. Blog Module (CRUD)

- Created Blog model with fields: title, content, author (ForeignKey to CustomUser), created_at, updated_at, is_published.
- Used ModelViewSet for API endpoints.
- Permissions Logic:
  - ADMIN: Full access (CRUD all blogs).
  - AUTHOR: Create blog, edit/delete own blogs.
  - READER: Can only view published blogs.

### 4. Custom Actions

- Added two custom actions using @action:
  - POST /blogs/{id}/publish/ (publishes a blog; allowed for ADMIN or owning AUTHOR).
  - GET /blogs/my-blogs/ (lists own blogs; allowed for AUTHOR only).

### 5. Database

- Used PostgreSQL (configurable for local or Railway hosting).
- Migration files provided in users/migrations/ and blogs/migrations/ (generated via makemigrations).
- Ensured clean schema with minimal, required fields only.

### 6. Management Command

- Created custom command: `python manage.py create_user <email> <password> <role>`.
- Allows creating users via CLI.
- Accepts role input (ADMIN, AUTHOR, READER).
- Hashes password properly using Django's set_password.

## Setup Instructions

### 1. Clone the Repository

```
git clone <your-repo-url>

```

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Configure Database (in blog_api/settings.py)

**For local PostgreSQL:**

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Create the DB:**

```
CREATE DATABASE blog_db;
```

### 5. Apply Migrations

```
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Test Users (via custom command)

```
python manage.py create_user admin@example.com admin123 ADMIN
python manage.py create_user author@example.com author123 AUTHOR
python manage.py create_user reader@example.com reader123 READER
```

### 7. Run the Server

```
python manage.py runserver
```

Access API at: `http://127.0.0.1:8000/api/`

## API Endpoints

### Authentication

- POST /api/token/ – Obtain access/refresh tokens (body: {"email": "...", "password": "..."}).
- POST /api/token/refresh/ – Refresh token.

### Blogs

- GET /api/blogs/ – List blogs (role-filtered).
- POST /api/blogs/ – Create blog (JSON body: {"title": "...", "content": "..."}).
- GET /api/blogs/<id>/ – Retrieve blog.
- PATCH /api/blogs/<id>/ – Update blog.
- DELETE /api/blogs/<id>/ – Delete blog.

### Custom Actions

- POST /api/blogs/<id>/publish/ – Publish a blog.
- GET /api/blogs/my-blogs/ – List own blogs.

All requests requiring auth use `Authorization: Bearer <access_token>` header.

## Testing

Manual testing was performed using Postman to verify all requirements, including role-based permissions and custom actions.

**Postman Setup:**

- Obtain tokens for each role via POST /api/token/.
- Use Bearer Token in headers.
- Test CRUD and actions per role.

**Key Scenarios:**

- ADMIN: CRUD all blogs.
- AUTHOR: CRUD own blogs only.
- READER: View published blogs only.
- Custom actions: Restricted by role.
- Unauthenticated: 401 on protected routes.


## Postman Published Documentation

https://documenter.getpostman.com/view/49639745/2sBXcDGLzd
