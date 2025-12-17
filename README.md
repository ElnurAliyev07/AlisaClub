# Alisa Club - Full-Stack Django Web Application

A Django-based web application for a children's club offering birthday party services, educational activities, and content management.

## Features

- **Multi-language Support**: Azerbaijani language interface
- **SEO Optimization**: Built-in SEO management with meta tags, Open Graph support
- **Content Management**: Dynamic content management for all sections
- **Blog System**: Full-featured blog with categories, media support, and gallery
- **Service Management**: Comprehensive service catalog with scheduling and FAQ
- **Event Management**: Birthday party booking and event coordination
- **User Profiles**: Parent profiles with child management and medal system
- **Admin Interface**: Enhanced Django admin with Jazzmin
- **Media Management**: Organized file handling with automatic image processing
- **Contact System**: Contact forms with Google Maps integration

## Technology Stack

- **Backend**: Django 4.x, Python 3.8+
- **Database**: SQLite (development), PostgreSQL ready
- **Admin**: Django Jazzmin for enhanced UI
- **Deployment**: Gunicorn WSGI server
- **Environment**: python-dotenv configuration

## Quick Setup

```bash
# Clone and setup
git clone <repository-url>
cd alisaclub
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Edit with your settings

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Project Structure

```
apps/
├── core/          # Site-wide settings, SEO, social links
├── home/          # Homepage content, hero, about sections
├── blog/          # Blog system with categories and media
├── services/      # Service management with features and FAQ
├── birthday/      # Birthday party booking system
├── contact/       # Contact forms and information
└── about/         # About page content

config/
├── settings/      # Environment-based configuration
├── urls.py        # URL routing
└── wsgi.py        # WSGI configuration
```

## Key Models

- **PageSEO**: SEO management for all pages
- **Blog**: Content management with media types and categories
- **Service**: Service catalog with features and scheduling
- **Event**: Birthday party and event management
- **ParentProfile**: User profile system with child management

## Production Deployment

```bash
# Environment setup
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/db

# Static files and database
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Run with Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## License

MIT License - see [LICENSE](LICENSE) file for details.