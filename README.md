# DevBlog

A portfolio-ready Django blog application with authentication, CRUD posts, categories, tags, search, pagination, comments, likes, bookmarks, profiles, image uploads, and a Bootstrap UI.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

## Features
- User registration/login/logout
- Author profiles and profile images
- Post CRUD with draft/published status
- Categories and tags
- Search and pagination
- Comments
- Likes and bookmarks
- View counter
- Related posts
- Responsive Bootstrap design
- Media uploads
