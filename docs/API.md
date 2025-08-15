# FastAPI Blog API Documentation

## Overview

The FastAPI Blog API provides a comprehensive REST API for blog management with user authentication and authorization. This document describes all available endpoints, request/response formats, and authentication requirements.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints, include the token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Getting an Access Token

1. Create a user account using `POST /users/`
2. Login using `POST /auth/login` or `POST /auth/login-form`
3. Use the returned `access_token` in subsequent requests

## Endpoints

### Authentication

#### POST /auth/login

Authenticate user and get access token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 30,
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "user@example.com",
    "is_active": true
  }
}
```

#### POST /auth/login-form

OAuth2 form-based authentication (for Swagger UI).

**Form Data:**
- `username`: User's email
- `password`: User's password

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 30
}
```

#### POST /auth/logout

Logout endpoint (client-side token removal).

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

#### GET /auth/me

Get current authenticated user information.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "user@example.com",
  "is_active": true,
  "is_verified": true
}
```

### Users

#### POST /users/

Create a new user account.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### GET /users/me

Get current user profile.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### GET /users/me/blogs

Get current user with their blog posts.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "blogs": [
    {
      "id": 1,
      "title": "My First Blog",
      "content": "This is my first blog post...",
      "summary": "A brief summary",
      "is_published": false,
      "creator_id": 1,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": null,
      "excerpt": "This is my first blog post..."
    }
  ]
}
```

#### PUT /users/me

Update current user information.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "John Smith",
  "email": "johnsmith@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "johnsmith@example.com",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

#### DELETE /users/me

Delete current user account.

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

### Blogs

#### POST /blogs/

Create a new blog post.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post...",
  "summary": "A brief summary of the blog post",
  "is_published": false
}
```

**Response:**
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post...",
  "summary": "A brief summary of the blog post",
  "is_published": false,
  "creator_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": null,
  "excerpt": "This is the content of my first blog post..."
}
```

#### GET /blogs/

Get all blogs with pagination.

**Query Parameters:**
- `skip` (int): Number of blogs to skip (default: 0)
- `limit` (int): Maximum number of blogs to return (default: 20, max: 100)
- `published_only` (bool): Show only published blogs (default: true)

**Response:**
```json
{
  "blogs": [
    {
      "id": 1,
      "title": "My First Blog Post",
      "content": "This is the content...",
      "summary": "A brief summary",
      "is_published": true,
      "creator_id": 1,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": null,
      "excerpt": "This is the content..."
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20,
  "has_next": false,
  "has_prev": false
}
```

#### GET /blogs/search

Search blogs by title or content.

**Query Parameters:**
- `q` (string): Search query (required)
- `skip` (int): Number of blogs to skip (default: 0)
- `limit` (int): Maximum number of blogs to return (default: 20, max: 100)

**Response:** Same format as `GET /blogs/`

#### GET /blogs/my-blogs

Get current user's blog posts.

**Headers:** `Authorization: Bearer <token>`

**Query Parameters:**
- `skip` (int): Number of blogs to skip (default: 0)
- `limit` (int): Maximum number of blogs to return (default: 20, max: 100)

**Response:** Same format as `GET /blogs/`

#### GET /blogs/{blog_id}

Get blog by ID with creator information.

**Response:**
```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content...",
  "summary": "A brief summary",
  "is_published": true,
  "creator_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": null,
  "excerpt": "This is the content...",
  "creator": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  }
}
```

#### PUT /blogs/{blog_id}

Update a blog post.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "title": "Updated Blog Title",
  "content": "Updated content...",
  "is_published": true
}
```

**Response:** Same format as blog creation

#### DELETE /blogs/{blog_id}

Delete a blog post.

**Headers:** `Authorization: Bearer <token>`

**Response:** `204 No Content`

#### POST /blogs/{blog_id}/publish

Publish a blog post.

**Headers:** `Authorization: Bearer <token>`

**Response:** Same format as blog creation

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": true,
  "message": "Error description",
  "status_code": 400
}
```

### Common HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content returned
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Rate Limiting

Currently, the API does not implement rate limiting. For production use, consider implementing rate limiting using Redis or similar solutions.

## Pagination

List endpoints support pagination using `skip` and `limit` parameters:

- `skip`: Number of items to skip (offset)
- `limit`: Maximum number of items to return

The response includes pagination metadata:
- `total`: Total number of items
- `page`: Current page number
- `size`: Page size
- `has_next`: Whether there are more pages
- `has_prev`: Whether there are previous pages

## Filtering

Some endpoints support filtering:

- `published_only`: Filter blogs by publication status
- Search functionality for blog content

## Sorting

Currently, the API returns items in creation order (newest first). Future versions may support custom sorting.

## Examples

### Complete Workflow

1. **Create User:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com", "password": "SecurePass123"}'
   ```

2. **Login:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "john@example.com", "password": "SecurePass123"}'
   ```

3. **Create Blog:**
   ```bash
   curl -X POST "http://localhost:8000/api/v1/blogs/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "My Blog", "content": "Blog content...", "is_published": false}'
   ```

4. **Get Blogs:**
   ```bash
   curl "http://localhost:8000/api/v1/blogs/"
   ```

5. **Update Blog:**
   ```bash
   curl -X PUT "http://localhost:8000/api/v1/blogs/1" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Title", "is_published": true}'
   ```

## Support

For API support and questions, please refer to the project documentation or open an issue on GitHub.
