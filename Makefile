# Development Environment
dev-up:
	@echo "🚀 Starting development environment with live reloading..."
	docker-compose -f docker-compose.dev.yml up -d
	@echo "✅ Development environment started!"
	@echo "🌐 API: http://localhost:8000"
	@echo "📚 Docs: http://localhost:8000/api/docs/"
	@echo "🔧 Admin: http://localhost:8000/admin/"
	@echo "🔄 Code changes will be reflected automatically!"

dev-down:
	@echo "🛑 Stopping development environment..."
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	@echo "📋 Showing development logs..."
	docker-compose -f docker-compose.dev.yml logs -f

dev-shell:
	@echo "🐚 Accessing development container shell..."
	docker-compose -f docker-compose.dev.yml exec rawad_backend bash

dev-rebuild:
	@echo "🔨 Rebuilding development containers..."
	docker-compose -f docker-compose.dev.yml build --no-cache

# Django Commands (for development)
migrate:
	@echo "🗃️  Running database migrations..."
	docker-compose -f docker-compose.dev.yml exec rawad_backend python manage.py migrate

makemigrations:
	@echo "📝 Creating new migrations..."
	docker-compose -f docker-compose.dev.yml exec rawad_backend python manage.py makemigrations

superuser:
	@echo "👤 Creating superuser..."
	docker-compose -f docker-compose.dev.yml exec rawad_backend python manage.py createsuperuser

collectstatic:
	@echo "📁 Collecting static files..."
	docker-compose -f docker-compose.dev.yml exec rawad_backend python manage.py collectstatic --noinput
