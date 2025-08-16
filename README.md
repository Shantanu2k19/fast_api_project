main → The bare-minimum template branch. Use this if you want a clean starting point with only the essentials.


# FastAPI Blog API

A scalable, production-ready FastAPI application for blog management with user authentication and authorization.

## Features

- **User Management**: User registration, authentication, and profile management
- **Blog Management**: Create, read, update, delete, and publish blog posts
- **Authentication**: JWT-based authentication with secure password hashing
- **Authorization**: Role-based access control and resource ownership validation
- **API Documentation**: Interactive API docs with Swagger UI and ReDoc
- **Error Handling**: Comprehensive error handling with consistent response formats
- **Logging**: Structured logging for monitoring and debugging
- **Validation**: Input validation using Pydantic schemas
- **Database**: SQLAlchemy ORM with support for multiple database backends

## Project Structure

```
app/
├── api/                    # API endpoints
│   └── v1/
│       ├── endpoints/      # Route handlers
│       │   ├── auth.py     # Authentication endpoints
│       │   ├── users.py    # User management endpoints
│       │   └── blogs.py    # Blog management endpoints
│       └── api.py          # Main API router
├── core/                   # Core functionality
│   ├── config.py           # Configuration management
│   ├── database.py         # Database configuration
│   ├── security.py         # Security utilities
│   └── exceptions.py       # Custom exceptions
├── models/                 # Database models
│   ├── user.py             # User model
│   └── blog.py             # Blog model
├── schemas/                # Pydantic schemas
│   ├── user.py             # User schemas
│   ├── blog.py             # Blog schemas
│   └── auth.py             # Authentication schemas
├── services/               # Business logic
│   ├── user_service.py     # User business logic
│   ├── blog_service.py     # Blog business logic
│   └── auth_service.py     # Authentication logic
└── main.py                 # Application entry point
```

## Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fast_api_project
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   python -m app.main
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Application Configuration
APP_NAME="FastAPI Blog API"
APP_VERSION="1.0.0"
DEBUG=false

# Database Configuration
DATABASE_URL="sqlite:///./blog.db"
DATABASE_ECHO=false

# Security Configuration
SECRET_KEY="your-super-secret-key-here-change-in-production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_HOSTS=["*"]
```

## Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using Python
```bash
python -m app.main
```

### Using Script
```bash
./start.py 
```

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/login-form` - OAuth2 form login
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user info

### Users
- `POST /api/v1/users/` - Create user account
- `GET /api/v1/users/me` - Get current user
- `GET /api/v1/users/me/blogs` - Get current user's blogs
- `PUT /api/v1/users/me` - Update current user
- `DELETE /api/v1/users/me` - Delete current user

### Blogs
- `POST /api/v1/blogs/` - Create blog post
- `GET /api/v1/blogs/` - Get all blogs (paginated)
- `GET /api/v1/blogs/search` - Search blogs
- `GET /api/v1/blogs/my-blogs` - Get user's blogs
- `GET /api/v1/blogs/{blog_id}` - Get blog by ID
- `PUT /api/v1/blogs/{blog_id}` - Update blog
- `DELETE /api/v1/blogs/{blog_id}` - Delete blog
- `POST /api/v1/blogs/{blog_id}/publish` - Publish blog

## Usage Examples

### 1. Create a User Account
```bash
curl -X POST "http://localhost:8000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### 3. Create a Blog Post
```bash
curl -X POST "http://localhost:8000/api/v1/blogs/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post...",
    "summary": "A brief summary of the blog post",
    "is_published": false
  }'
```

## Development

### Code Quality Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Linting
```bash
flake8 app/
mypy app/
```

## Database Migrations

The application uses SQLAlchemy with automatic table creation. For production use, consider using Alembic for database migrations:

```bash
# Initialize Alembic
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Security Features

- **Password Hashing**: Bcrypt-based password hashing
- **JWT Tokens**: Secure token-based authentication
- **Input Validation**: Comprehensive input validation using Pydantic
- **CORS Protection**: Configurable CORS middleware
- **Rate Limiting**: Ready for rate limiting implementation
- **SQL Injection Protection**: SQLAlchemy ORM protection

## Scalability Features

- **Modular Architecture**: Clean separation of concerns
- **Service Layer**: Business logic separated from API layer
- **Dependency Injection**: FastAPI's dependency injection system
- **Async Support**: Full async/await support
- **Database Connection Pooling**: Efficient database connections
- **Caching Ready**: Structure ready for Redis/Memcached integration

## Monitoring and Logging

- **Structured Logging**: JSON-formatted logs
- **Request Timing**: Response time headers
- **Health Checks**: `/health` endpoint
- **Error Tracking**: Comprehensive error handling and logging

## Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
Set appropriate environment variables for production:
- `SECRET_KEY`: Use a strong, random secret key
- `DATABASE_URL`: Use production database
- `DEBUG`: Set to `false`
- `ALLOWED_HOSTS`: Restrict to your domain

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Ensure code quality tools pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue on GitHub. 
