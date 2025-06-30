# Rwad Al Furas - Job Matching, Freelance & Donation System Backend

A comprehensive platform that connects job seekers, job publishers, and supporters through an integrated system featuring job matching, freelance project management, and community donation initiatives.

## 🌟 Platform Overview

This system serves four main user types:
- **Job Seekers**: Professionals looking for employment opportunities
- **Job Publishers**: Companies and individuals posting job opportunities  
- **Supporters**: Community members contributing to donation initiatives
- **Admin**: Platform administrators managing the entire ecosystem

## 🚀 Features

### 👤 Job Seeker Module

#### Registration & Authentication
- **Registration Fields**: Full name, email, specialization, field of work, date of birth, mobile number, password confirmation
- **Login**: Email and password authentication
- **Password Recovery**: Email-based password reset functionality

#### Dashboard Features
1. **Profile Management**
   - Personal information (name, photo, specialization, field of work)
   - Experience level and bio
   - 5-star rating system ⭐
   - Availability status (available for work or not)
   - Expected hourly rate
   - Edit and save functionality

2. **Services Portfolio**
   - Service descriptions and work samples
   - Portfolio management with edit/save capabilities

3. **Job Opportunities**
   - **Filters**: 
     - All categories or specific category
     - Latest posted jobs
     - Part-time vs full-time positions
     - Hourly rate vs monthly salary
   - **Application Limits**: Maximum 5 job applications per week
   - **Job Details**: Company name/logo, position title, requirements, employment type, location, application deadline
   - **Actions**: Apply, save to favorites, share via link or social media

4. **Application Tracking**
   - Track weekly applications
   - Color-coded status system:
     - Yellow: Active applications (within the week)
     - Red: Expired applications (after a week without acceptance)

5. **Notifications & Inbox**
   - Job acceptance notifications
   - Admin communications
   - System announcements

6. **Employment Status**
   - When hired, company contacts platform support
   - Application opportunities are frozen
   - Employment badge displayed on profile

7. **Technical Support**
   - Contact admin interface with title, description, and message fields

8. **Co-working Spaces**
   - Nearby workspace listings
   - Owner contact information
   - Power and high-speed internet availability hours

9. **Settings**
   - Password management
   - Dark mode toggle

### 🏢 Job Publisher Module

#### Registration Types
1. **Company Registration**
   - Company name, location, type (marketing, programming, etc.)
   - License number, email, mobile, password confirmation

2. **Business Owner Registration**
   - Full name, mobile, email, password confirmation

3. **Individual Client Registration**
   - Full name, mobile, email, password confirmation

#### Company Dashboard
1. **Company Profile**
   - Company information (name, logo, field, size, headquarters)
   - Website and LinkedIn links
   - Company bio and services description

2. **Job Posting**
   - Job title, description, requirements
   - Employment type (full-time/part-time)
   - Salary structure (monthly salary or hourly rate)
   - Application deadline
   - External application link and HR email

3. **Posted Jobs Management**
   - View all published jobs
   - Filter by date range
   - Edit and republish functionality

4. **Freelance Project Management**
   - Project name, description, requirements
   - Required technologies
   - Direct documentation upload capability

5. **Published Projects**
   - Manage all freelance projects
   - Edit and republish functionality

6. **Technical Support**
   - Direct communication with platform support
   - Structured messaging system

7. **Settings**
   - Password management
   - Dark mode
   - Notification inbox

#### Individual Client Dashboard
1. **Personal Profile**
   - Photo (optional), full name, location
   - Business information (if applicable)
   - Social media links, email, mobile

2. **Work Posting**
   - **Service Type**: Choose between service or system development
   - **Service Details**: Name, description, proposed price, delivery timeline
   - **System Development**: Application, website, or desktop software
   - **System Requirements**: Full description or documentation upload

3. **Project Management**
   - Edit and republish posted projects/services

4. **Technical Support**
   - Platform communication system

5. **Settings**
   - Password and dark mode management
   - Notification inbox

### 💝 Supporter Module

#### Registration & Authentication
- Full name, country, mobile number with country code
- Email and password confirmation
- Email/password login system

#### Supporter Dashboard
1. **Profile Management**
   - Personal information display
   - Achievement badges based on donation frequency and amounts
   - Color-coded recognition system

2. **Initiative Browsing**
   - **Filters**:
     - Latest initiatives
     - Price range ($500-$1000, $1000-$5000, etc.)
     - Initiative type (technical, community, humanitarian)
   - **Progress Tracking**: Visual indicators showing funding progress toward goals
   - **Donation Process**: Multiple payment method options

3. **Completed Initiatives**
   - Photo galleries with descriptions
   - Success stories and impact reports

4. **Technical Support**
   - Direct platform communication

5. **Feedback System**
   - Initiative feedback and interaction capabilities

6. **Settings**
   - Password management
   - Dark mode
   - Notification inbox

### 🔧 Admin Dashboard

#### Authentication
- Email and password login only

#### Management Features
1. **User Management**
   - **Job Seekers**: View, delete, or disable accounts
   - **Job Publishers**: Account management capabilities
   - **Supporters**: Account management plus badge assignment based on donation history

2. **Project Evaluation**
   - Review projects/services from companies and individuals
   - Send price quotes via email
   - Contract negotiation and agreement management

3. **Initiative Management**
   - **Create Initiatives**: Name, description, purpose, target amount, type, date
   - **Documentation**: Add photos for completed initiatives
   - **Tracking**: Monitor completed vs. in-progress initiatives
   - **Management**: Edit and republish initiatives

4. **Settings**
   - Password management
   - Dark mode

## 🛠 Technical Stack

- **Backend Framework**: Django 5.2+ with Django REST Framework
- **Database**: PostgreSQL 17
- **Cache & Message Broker**: Redis 8.0
- **Task Queue**: Celery
- **Authentication**: JWT with django-rest-framework-simplejwt
- **API Documentation**: DRF Spectacular (OpenAPI/Swagger)
- **File Handling**: Django file upload with Pillow for images
- **Containerization**: Docker with Docker Compose
- **Web Server**: Nginx (production)
- **WSGI Server**: Gunicorn (production)

## 📋 Development Requirements

### Core Features to Implement
- [ ] User authentication system for all user types
- [ ] Role-based access control (RBAC)
- [ ] Job posting and application system
- [ ] Freelance project management
- [ ] Donation initiative platform
- [ ] File upload and management
- [ ] Email notification system
- [ ] Real-time notifications
- [ ] Search and filtering capabilities
- [ ] Payment integration for donations
- [ ] Admin dashboard with full management capabilities
- [ ] API documentation and testing
- [ ] Security implementations (rate limiting, input validation)
- [ ] Mobile-responsive design considerations

### API Endpoints Structure
- `/api/auth/` - Authentication endpoints
- `/api/users/` - User management
- `/api/jobs/` - Job postings and applications
- `/api/projects/` - Freelance projects
- `/api/initiatives/` - Donation initiatives
- `/api/admin/` - Admin-only endpoints
- `/api/notifications/` - Notification system
- `/api/support/` - Technical support

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Docker and Docker Compose
- PostgreSQL 17
- Redis 8.0

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd Rwad-Al-Furas-Job-Matching-Freelance-Donation-System-Backend

# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# Run migrations
docker-compose -f docker-compose.dev.yml exec rwad_furas_backend python manage.py migrate

# Create superuser
docker-compose -f docker-compose.dev.yml exec rwad_furas_backend python manage.py createsuperuser
```

### Production Deployment
```bash
# Start production environment
docker-compose up --build -d

# Collect static files
docker-compose exec rwad_furas_backend python manage.py collectstatic --noinput
```

## 📚 API Documentation

API documentation is available at:
- Development: `http://localhost:8000/api/schema/swagger-ui/`
- Production: `https://api.rwad-furas.com/api/schema/swagger-ui/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Analysis & Development

**Analysis By**: Eng Adham Saed, Computer Engineer

---

*Building bridges between talent and opportunity while fostering community support through technology.*
