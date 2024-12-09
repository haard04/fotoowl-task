# Library Management System 🏛️

## Overview
Django-powered Library Management API with user authentication, book catalog, and book request workflows for Assesment task of Fotoowl AI.

## Features
- User registration and authentication
- Book catalog management
- Book borrowing request system
- Role-based access control (Librarian/User)
- Request approval/denial workflow
- CSV export of book request history

## Tech Stack
- Django
- Django Rest Framework
- Custom User Authentication
- PostgreSQL (recommended)

## Setup & Installation

### Prerequisites
- Python 3.9+
- Django 4.2+
- pip

### Installation Steps
```bash
git clone https://github.com/haard04/fotoowl-task
cd library_managem
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API Endpoints

### Authentication
- `/api/user/register/` - User registration
- `/api/user/login/` - User login

### Books
- `/api/books/` - List books
- `/api/books/create/` - Create book
- `/api/books/<id>/` - Book details

### Book Requests
- `/api/book-request/create/` - Create book request
- `/api/book-request/list/` - List book requests
- `/api/book-request/history/` - Download request history

## Postman Collection
[![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/21423387/2sAYBd88BS)
