# 🚀 Django REST API Production Template

A comprehensive, production-ready Django REST Framework template with modern Python 3.13, containerized architecture, and best practices for scalable web applications.

## ⭐ Features

### 🏗️ **Modern Architecture**
- **Django 5.2+** with REST Framework
- **Python 3.13** with UV package manager for blazing-fast dependency management
- **PostgreSQL 17** with optimized connection pooling
- **Redis 8.0** for caching and message brokering
- **Celery** for asynchronous task processing
- **Nginx 1.27** reverse proxy with compression and security headers
- **Gunicorn** WSGI server with optimized worker configuration

### 🐳 **Docker & DevOps**
- **Multi-stage Docker builds** for production optimization
- **Docker Compose** for both development and production environments
- **Live code reloading** in development with volume mounting
- **Health checks** and graceful shutdowns
- **Separate development/production configurations**

### 🔐 **Security & Authentication**
- **JWT authentication** with refresh tokens
- **CORS configuration** for cross-origin requests
- **Security headers** (HSTS, XSS protection, content type sniffing)
- **Session security** with HttpOnly cookies
- **Environment-based configuration** with Pydantic settings

### 📚 **API Documentation**
- **Swagger/OpenAPI** documentation with drf-spectacular
- **ReDoc** alternative documentation interface
- **Standardized API responses** with consistent error handling
- **Health check endpoints** for monitoring

### 🔄 **Task Queue & Caching**
- **Celery workers** with Redis broker
- **Task routing** to different queues (emails, media, reports)
- **Redis caching** with django-redis
- **Session storage** in Redis for scalability

### 🛠️ **Development Experience**
- **Hot reloading** for both Django and Celery
- **Django Debug Toolbar** with comprehensive panels
- **Makefile** with convenient development commands
- **Code quality tools** (Black, isort, flake8)
- **Comprehensive logging** configuration

### 📁 **File Handling**
- **WhiteNoise** for static file serving
- **Media file management** with proper permissions
- **File upload optimization** with size limits

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.13+ (for local development)
- UV package manager (optional but recommended)

### 1. Clone and Setup
```bash
# Clone the template
git clone <your-repo-url>
cd django-rest-template

# Copy environment configuration
cp .env.example .env
# Edit .env with your settings
```

### 2. Development Environment
```bash
# Start all services (PostgreSQL, Redis, Django, Celery)
docker-compose -f docker-compose.dev.yml up -d

# Run migrations
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate

# Create superuser
docker-compose -f docker-compose.dev.yml exec backend python manage.py createsuperuser

# Access your application
# API: http://localhost:8000
# Docs: http://localhost:8000/api/docs/
# Admin: http://localhost:8000/admin/
```

### 3. Production Deployment
```bash
# Build production containers
docker-compose build

# Deploy with optimized settings
docker-compose up -d
```

## 📋 Available Commands

The template includes a comprehensive Makefile for easy development:

```bash
# Development
make dev-up          # Start development environment
make dev-down        # Stop development environment
make dev-logs        # View logs
make dev-shell       # Access container shell

# Django Management
make migrate         # Run database migrations
make makemigrations  # Create new migrations
make superuser       # Create admin user
make collectstatic   # Collect static files

# Code Quality
make test           # Run tests
make lint           # Run linting
make format         # Format code (Black + isort)

# Production
make prod-build     # Build production containers
make prod-up        # Start production environment
make prod-down      # Stop production environment
```

## 🏗️ Architecture Overview

### Container Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │  Django + DRF   │    │ Celery Workers  │
│   (Port 80/443) │───▶│   (Port 8000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  PostgreSQL 17  │    │    Redis 8.0    │    │    Static/Media │
│   (Port 5432)   │    │   (Port 6379)   │    │      Files      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Components
- **API Layer**: Django REST Framework with JWT authentication
- **Database**: PostgreSQL with connection pooling
- **Cache**: Redis for sessions, cache, and Celery broker
- **Tasks**: Celery workers for background processing
- **Proxy**: Nginx for static files, SSL termination, and load balancing
- **Documentation**: Auto-generated API docs with Swagger/ReDoc

## 🔧 Configuration

### Environment Variables
Key settings in `.env`:
```bash
# Django Core
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
POSTGRES_NAME=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password

# Redis
REDIS_PASSWORD=your_redis_password

# Security
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Settings Structure
- `base.py` - Common settings for all environments
- `development.py` - Development-specific overrides
- `production.py` - Production security and optimizations
- `config.py` - Environment variable management with Pydantic

## 📚 API Documentation

### Endpoints
- **Health Check**: `GET /health/`
- **API Root**: `GET /api/`
- **Authentication**: `POST /api/auth/token/`
- **Token Refresh**: `POST /api/auth/token/refresh/`
- **API Schema**: `GET /api/schema/`
- **Swagger Docs**: `GET /api/docs/`
- **ReDoc**: `GET /api/redoc/`

### Adding New Apps
1. Create Django app: `python manage.py startapp your_app`
2. Add to `LOCAL_APPS` in `settings/base.py`
3. Create URLs and include in `core/urls.py`
4. Build your models, serializers, and views

## 🔄 Celery Tasks

### Task Examples
```python
from core.tasks import send_email_task

# Send email asynchronously
send_email_task.delay(
    subject="Welcome!",
    message="Welcome to our platform",
    recipient_list=["user@example.com"]
)
```

### Task Queues
- **emails**: Email sending tasks
- **media**: Image/file processing
- **reports**: Report generation
- **default**: General background tasks

## 🛡️ Security Features

- **HTTPS ready** with SSL/TLS configuration
- **Security headers** (HSTS, XSS protection, CSRF)
- **CORS configuration** for API access
- **JWT tokens** with automatic refresh
- **Session security** with secure cookies
- **Input validation** and sanitization
- **Rate limiting ready** (easily configurable)

## 🚀 Production Optimizations

- **Multi-stage Docker builds** for smaller images
- **Static file compression** with WhiteNoise
- **Database connection pooling**
- **Redis connection optimization**
- **Gunicorn worker tuning**
- **Nginx caching and compression**
- **Health check endpoints**
- **Graceful shutdowns**

## 📊 Monitoring & Logging

- **Structured logging** with configurable levels
- **Health check endpoints** for load balancers
- **Database query monitoring** (in development)
- **Celery task monitoring** with built-in tools
- **Error tracking ready** (easily integrate Sentry)

## 🧪 Testing

```bash
# Run tests
make test

# Run with coverage
uv run pytest --cov=.

# Run specific test
uv run pytest apps/your_app/tests/
```

## 📝 Code Quality

The template includes pre-configured code quality tools:
- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **pytest**: Testing framework

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django REST Framework team for the excellent API framework
- Celery team for robust task queue implementation
- Redis team for blazing-fast caching and messaging
- Docker team for containerization excellence

## 📞 Support

- **Documentation**: Check the `/api/docs/` endpoint for API documentation
- **Issues**: Open an issue on GitHub for bug reports
- **Discussions**: Use GitHub Discussions for questions and ideas

---

**⭐ If this template helped you, please give it a star!**

Built with ❤️ for the Django community
