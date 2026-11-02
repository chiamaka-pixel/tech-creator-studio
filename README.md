# Tech Creator Studio

Tech Creator Studio is a Django-based content management application designed to help content creators organise, manage, schedule and track their social media content.

The project is being developed as a practical software engineering project.

## Features

### Content Management
- Create content items.
- Edit existing content.
- View detailed content information.
- Organise content by category.
- Track content status.
- Manage captions, hashtags and production notes.
- Select content format and publishing platform.

### Recycle Bin
- Move deleted content into the Recycle Bin.
- Restore deleted content.
- Permanently delete individual items.
- Empty the Recycle Bin.

### Research Management
- Add research source links.
- Edit existing source links.
- Remove source links.
- Store publication dates and research notes.

### Content Calendar
- View scheduled content by month.
- Navigate between months.
- Identify today's date.
- Open scheduled content directly from the calendar.

### Content Performance
- Record reach and views.
- Track likes, comments and shares.
- Calculate total interactions.
- Calculate engagement rate.
- View overall performance statistics.
- Identify top-performing content.

## Technology Stack

- Python
- Django
- HTML
- CSS
- SQLite
- Git and GitHub

## Project Structure

```text
tech-creator-studio/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── content/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── source_forms.py
│   ├── performance_forms.py
│   └── performance_views.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md