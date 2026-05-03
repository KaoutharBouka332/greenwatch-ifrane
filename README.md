# GreenWatch Ifrane

GreenWatch is a Django-based environmental monitoring web platform for the Province of Ifrane. It allows citizens to anonymously report environmental incidents such as forest fires, illegal logging, water leaks, and pollution using an interactive map.

Authorities can securely log in, review submitted reports, validate incidents, update statuses, and manage response actions through a dedicated dashboard.

## Features

- Anonymous citizen incident reporting
- Interactive map-based location selection
- Image attachment upload
- Incident tracking using public tokens
- Authority login and restricted dashboard
- Report validation and status management
- Responsive modern UI with icons and colors

## Tech Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Map: Leaflet
- Database: SQLite for development
- Version Control: Git and GitHub

## Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
