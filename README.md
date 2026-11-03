# Tech Creator Studio

Tech Creator Studio is a Django content workspace for creating, organising, scheduling and measuring social content.

## Workspace pages
- Dashboard with current content totals, reach, interactions, upcoming items and recent activity.
- Content Library at `/library/` with status and text search filters.
- Content creation, editing and detailed review pages.
- Monthly content calendar.
- Performance entry and overview dashboard.
- Research source library and item-specific source links.
- Recycle Bin with restore and permanent-delete actions.
- Settings for account summary and browser-saved light/dark appearance.
- Help & Support guides.
- Custom sign-in page using the existing Django user accounts.

## Design system
Electric orange `#FF6500`, lemon `#D8FF24`, near-black `#050505`, and soft ivory `#F5F4EF`. Light and dark modes are both supported.

## Technology
Python, Django, HTML, CSS, JavaScript and SQLite. n8n is part of the planned automation integration but is not connected in this snapshot.

## Local run
Activate the existing virtual environment, then run `python manage.py check`, `python manage.py test`, and `python manage.py runserver`.
