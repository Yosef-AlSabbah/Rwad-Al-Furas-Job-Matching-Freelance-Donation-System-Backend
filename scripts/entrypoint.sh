#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Rawad Al Furas Backend Service${NC}"

# Function to wait for service
wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3

    echo -e "${YELLOW}⏳ Waiting for $service_name...${NC}"
    while ! nc -z $host $port; do
        sleep 1
    done
    echo -e "${GREEN}✅ $service_name is ready!${NC}"
}

# Wait for database
wait_for_service ${POSTGRES_HOST:-rawad_database} ${POSTGRES_PORT:-5432} "PostgreSQL Database"

# Wait for Redis
wait_for_service ${REDIS_HOST:-rawad_redis} ${REDIS_PORT:-6379} "Redis Cache"

# Activate virtual environment
source .venv/bin/activate

echo -e "${YELLOW}📦 Running database migrations...${NC}"
python manage.py migrate --noinput

echo -e "${YELLOW}📊 Collecting static files...${NC}"
python manage.py collectstatic --noinput --clear

echo -e "${YELLOW}👤 Creating superuser if needed...${NC}"
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@rawad.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

echo -e "${GREEN}🎯 Starting application...${NC}"

# Execute the main command
exec "$@"
