# Expense Splitter

A Django-based web application for managing and splitting expenses among group members. Users can create groups, add expenses, and automatically calculate balances for fair splitting.

## Features

- User registration and authentication
- Create and manage expense groups
- Add expenses with categories and participants
- Automatic balance calculation for equal splits
- Admin dashboard with statistics and activity feed
- Responsive web interface

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd expense-splitter
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser (optional, for admin access):
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Open your browser and go to `http://127.0.0.1:8000/`

## Usage

1. Register a new account or login
2. Create a new group and add members
3. Add expenses to the group, specifying amount, category, and participants
4. View balance summaries to see who owes what
5. Access the admin panel at `/admin/` for advanced management

## Project Structure

```
expense_splitter/
├── expense_splitter/          # Main Django project settings
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── expenses/                 # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # App URL patterns
│   ├── utils.py             # Utility functions
│   ├── admin.py             # Admin interface
│   ├── apps.py              # App configuration
│   ├── signals.py           # Django signals
│   ├── tests.py             # Unit tests
│   ├── migrations/          # Database migrations
│   ├── static/              # Static files (CSS, JS)
│   └── templates/           # HTML templates
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── .gitignore              # Git ignore file
```

## API Endpoints

- `/api/dashboard/` - JSON dashboard data
- `/api/group/<id>/balances/` - Group balance data
- `/api/admin-activity-feed/` - Admin activity feed
- `/api/admin-stats/` - Admin statistics

## Technologies Used

- Django 5.2
- SQLite (default database)
- Bootstrap (for styling)
- Python 3.8+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is licensed under the MIT License.
