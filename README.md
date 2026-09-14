# Django - Documentation 

Django is a high-level Python web framework that follows the **MVT (Model-View-Template)** architectural pattern. It handles URL routing, database access (ORM), templating, forms, authentication, and admin interfaces out of the box, following the "batteries-included" philosophy.

---

## 1. Installation & Environment Setup

```bash
# Create a virtual environment (isolates project dependencies)
python -m venv venv

# Activate it
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# Install Django
pip install django

# Check version
django-admin --version
```

**Why a virtual environment?** Each project can use a different Django/package version without conflicting with other projects on your system.

---

## 2. What is a Django "Project"?

A **project** is the entire web application container — it holds global settings, the root URL configuration, and one or more "apps." Think of it as the house; apps are the rooms.

### Create a project

```bash
django-admin startproject myproject .
```

The trailing `.` puts project files in the current directory instead of creating a nested extra folder. Omit it if you want a nested structure.

### Resulting structure

```
myproject/
├── manage.py
└── myproject/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── asgi.py
    └── wsgi.py
```

- **`myproject/settings.py`** — the project's central configuration (database, installed apps, middleware, templates, static files, etc.)
- **`myproject/urls.py`** — the root URL router that dispatches requests to apps.
- **`myproject/wsgi.py`** — entry point for WSGI-compatible web servers (used in traditional deployment).
- **`myproject/asgi.py`** — entry point for ASGI servers (used for async support, WebSockets).

---

## 3. What is `manage.py`?

`manage.py` is a command-line utility auto-generated with every project. It's a thin wrapper around Django's `django-admin` that's pre-configured to know which settings module to use. **You run almost every Django command through it.**

Common usage:

```bash
python manage.py <command>
```

---

## 4. What is a Django "App"?

An **app** is a self-contained module that does one specific thing — e.g., a `blog` app, a `users` app, a `payments` app. A project can (and usually does) contain many apps. Apps are reusable — you could theoretically drop the same app into a different project.

**Project vs App — the core distinction:**
| Project | App |
|---|---|
| The whole website/configuration | A specific feature/functionality |
| One per codebase | Many per project |
| Holds settings.py, root urls.py | Holds models, views, its own urls, templates |

### Create an app

```bash
python manage.py startapp blog
```

### Resulting structure

```
blog/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

Note: `urls.py` and a `templates/` folder are **not** auto-created — you create them yourself (explained below).

### Register the app

Every app must be registered in `settings.py` before Django recognizes it:

```python
# myproject/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blog',   # <-- your app
]
```

---

## 5. What are Models?

A **model** is a Python class that maps to a database table (Django's ORM — Object-Relational Mapper). Each attribute represents a database column. You write Python; Django generates the SQL.

```python
# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
```

**Common field types:** `CharField`, `TextField`, `IntegerField`, `BooleanField`, `DateField`, `DateTimeField`, `ForeignKey`, `ManyToManyField`, `OneToOneField`, `EmailField`, `ImageField`, `FileField`, `SlugField`, `DecimalField`.

**Common field options:** `max_length`, `default`, `null`, `blank`, `unique`, `choices`, `on_delete`.

### Migrations — turning models into database tables

```bash
python manage.py makemigrations   # Generates migration files from model changes
python manage.py migrate          # Applies migrations to the actual database
```

- `makemigrations` — Django looks at your models and writes a "diff" file describing schema changes.
- `migrate` — actually executes that diff against the database (creates/alters tables).

You **always** run both, in that order, after changing `models.py`.

---

## 6. What is `urls.py`?

A **URL configuration (URLconf)** maps URL patterns to views — it decides "which Python function/class runs when a user visits this URL."

### Root URLconf (project-level)

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),   # delegate to the app's own urls.py
]
```

### App-level URLconf

```python
# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'  # namespacing, used in {% url %} tags

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]
```

**Path converters:** `<int:id>`, `<str:name>`, `<slug:slug>`, `<uuid:id>`, `<path:subpath>`.

---

## 7. What are Views?

A **view** is a Python function (or class) that receives an HTTP request and returns an HTTP response. It contains the business logic — fetching data, processing forms, deciding what to render.

### Function-based view (FBV)

```python
# blog/views.py
from django.shortcuts import render, get_object_or_404

from .models import Post

def post_list(request):
    posts = Post.objects.filter(published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    return render(request, 'blog/post_detail.html', {'post': post})
```

### Class-based view (CBV) — alternative style

```python
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
```

CBVs reduce boilerplate for common patterns (list, detail, create, update, delete) via generic views: `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`.

---

## 8. What are Templates?

**Templates** are HTML files with embedded Django Template Language (DTL) tags — used to dynamically render data passed from a view. This is the "T" in MVT.

### Setup

Create a `templates/` folder inside your app (or a project-level one):

```
blog/
└── templates/
    └── blog/
        ├── base.html
        ├── post_list.html
        └── post_detail.html
```

Namespacing templates inside an app-named subfolder (`blog/templates/blog/...`) avoids name clashes between apps.

Ensure `settings.py` is configured to find them:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # optional project-level templates dir
        'APP_DIRS': True,                    # tells Django to look inside each app's templates/ folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Template syntax essentials

```html
<!-- base.html -->
<!DOCTYPE html>
<html>
<head><title>{% block title %}My Site{% endblock %}</title></head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
```

```html
<!-- post_list.html -->
{% extends "blog/base.html" %}

{% block content %}
  {% for post in posts %}
    <h2><a href="{% url 'blog:post_detail' post.slug %}">{{ post.title }}</a></h2>
    <p>{{ post.content|truncatewords:30 }}</p>
  {% empty %}
    <p>No posts yet.</p>
  {% endfor %}
{% endblock %}
```

**Key syntax:**
- `{{ variable }}` — output a variable
- `{% tag %}` — logic (loops, conditionals, includes, template inheritance)
- `{{ value|filter }}` — transform output (`date`, `truncatewords`, `lower`, `default`, `length`)
- `{% extends %}` / `{% block %}` — template inheritance
- `{% include %}` — insert a sub-template
- `{% url 'name' arg %}` — reverse-resolve a URL by its name (avoids hardcoding paths)
- `{% csrf_token %}` — required inside every `<form method="post">`
- `{% static 'path' %}` — link static files (requires `{% load static %}` at the top)

---

## 9. What is Jinja (Jinja2) — and how it relates to Django

**Jinja2** is a separate, general-purpose Python templating engine (also used by Flask). It is **not** Django's default engine — Django ships its own template engine (DTL, shown above). However, Django can be configured to use Jinja2 instead, because Jinja2 is faster and has more Python-like syntax (e.g., function calls, more flexible expressions).

**Differences:**
| Django Template Language | Jinja2 |
|---|---|
| `{{ value\|filter:"arg" }}` | Same filter syntax, but supports full function calls: `{{ func(arg) }}` |
| No arbitrary Python expressions | Allows more Python-like expressions |
| Safer by default (limited logic in templates, intentional) | More powerful/flexible, less restrictive |
| Slower | Faster (compiles to Python bytecode) |

### Enabling Jinja2 in Django (optional)

```bash
pip install Jinja2
```

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR / 'jinja2'],
        'APP_DIRS': True,
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        # ... keep DTL as well for admin, which requires it
    },
]
```

Django's own admin site **requires** DTL, so you typically keep both engines registered simultaneously if you introduce Jinja2 — Jinja2 for your app templates, DTL for admin.

**In practice:** most Django projects stick with the default DTL unless there's a specific performance/flexibility need — it's tightly integrated with forms, admin, and the wider ecosystem.

---

## 10. The Development Server

```bash
python manage.py runserver          # http://127.0.0.1:8000/
python manage.py runserver 8080     # custom port
python manage.py runserver 0.0.0.0:8000   # accessible on your local network
```

This is a lightweight server for development only — never use it in production (use Gunicorn/uWSGI behind Nginx instead).

---

## 11. Superuser & the Admin Site

### What is `admin`?

Django ships with a built-in, auto-generated **admin interface** (`django.contrib.admin`) — a ready-made dashboard to create/read/update/delete database records through a web UI, without writing any views yourself. It's one of Django's signature features.

### Create a superuser

```bash
python manage.py createsuperuser
```

You'll be prompted for username, email, and password. This account can log into `/admin/` with full permissions.

### Register a model to appear in admin

```python
# blog/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'created_at')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
```

Without registration, a model exists in the database but won't show up in `/admin/`.

Visit: `http://127.0.0.1:8000/admin/` and log in with the superuser credentials.

---

## 12. Static Files & Media Files

**Static files** = CSS, JS, images that are part of your app's design (fixed, not user-uploaded).
**Media files** = files uploaded by users at runtime (e.g., profile pictures).

```python
# settings.py
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']       # your source static files during development
STATIC_ROOT = BASE_DIR / 'staticfiles'         # where `collectstatic` gathers everything for production

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

```python
# myproject/urls.py (development only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

```bash
python manage.py collectstatic   # gathers all static files into STATIC_ROOT for deployment
```

---

## 13. Integrating Tailwind CSS with Django

There are two common approaches. The **django-tailwind** package (recommended, most popular) is shown below.

### Option A — `django-tailwind` package

```bash
pip install django-tailwind
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'tailwind',
    'theme',          # the app you'll create below
    'django_browser_reload',  # optional, for live-reload during dev
]

TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = ["127.0.0.1"]  # required by django_browser_reload
```

```bash
python manage.py tailwind init      # creates a 'theme' app with Tailwind config
```

Register the generated `theme` app (as shown above), then:

```bash
python manage.py tailwind install   # installs npm dependencies (needs Node.js installed)
python manage.py tailwind start     # runs Tailwind's watcher during development
```

In your base template:

```html
{% load tailwind_tags %}
<!DOCTYPE html>
<html>
<head>
    {% tailwind_css %}
</head>
<body class="bg-gray-100 text-gray-900">
    ...
</body>
</html>
```

For production:

```bash
python manage.py tailwind build     # generates the minified production CSS
```

### Option B — Tailwind via CDN (fastest, dev/prototyping only, not recommended for production)

```html
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
```

No build step needed, but you lose PurgeCSS optimization, custom config, and plugin support — fine for quick prototypes, not production.

### Option C — Standalone Tailwind CLI (no Node/npm project needed)

```bash
# Download the standalone Tailwind CLI binary from the Tailwind releases page, then:
./tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch
```

Link `output.css` as a normal static file in your templates. This avoids setting up a full `django-tailwind` app if you just want raw Tailwind without the wrapper package.

---

## 14. Settings.py — the Important Bits

```python
DEBUG = True                  # NEVER True in production — leaks stack traces
ALLOWED_HOSTS = []             # must list your domain(s) when DEBUG=False
SECRET_KEY = '...'             # keep this secret; used for cryptographic signing

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # default; swap for postgresql/mysql in production
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Example: PostgreSQL config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**Middleware** = a chain of request/response processors (each request passes through them in order; each response passes back through in reverse).

---

## 15. Django Shell (interactive ORM testing)

```bash
python manage.py shell
```

```python
>>> from blog.models import Post
>>> Post.objects.all()
>>> Post.objects.filter(published=True).count()
>>> Post.objects.create(title="Hello", content="World", author_id=1)
>>> post = Post.objects.get(id=1)
>>> post.title = "Updated"
>>> post.save()
>>> post.delete()
```

**Common QuerySet methods:** `.all()`, `.filter()`, `.exclude()`, `.get()`, `.order_by()`, `.count()`, `.first()`, `.last()`, `.values()`, `.annotate()`, `.aggregate()`.

---

## 16. Forms

```python
# blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'published']
```

```python
# blog/views.py
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})
```

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```

`ModelForm` auto-generates form fields from a model — huge time saver over writing plain `forms.Form` fields manually.

---

## 17. Full Command Cheat Sheet

```bash
django-admin startproject <name> [.]     # create a new project
python manage.py startapp <name>         # create a new app

python manage.py runserver [port]        # start dev server

python manage.py makemigrations [app]    # create migration files
python manage.py migrate [app]           # apply migrations
python manage.py sqlmigrate app 0001     # preview SQL for a migration
python manage.py showmigrations          # list migration status

python manage.py createsuperuser         # create admin account
python manage.py changepassword <user>   # reset a user's password

python manage.py shell                   # interactive Python shell with Django loaded
python manage.py dbshell                 # opens your database's own CLI

python manage.py collectstatic           # gather static files for deployment
python manage.py test                    # run test suite
python manage.py check                   # sanity-check the project for errors

python manage.py dumpdata > data.json    # export DB data as fixtures
python manage.py loaddata data.json      # import fixtures into DB
```

---

## 18. Full Request Lifecycle (Putting It All Together)

1. Browser sends a request to a URL, e.g. `/post/my-first-post/`.
2. **`urls.py`** (root) matches the pattern and delegates to the app's `urls.py`.
3. The app's **`urls.py`** matches `post/<slug:slug>/` and calls the corresponding **view**.
4. The **view** queries the **model** (ORM → database) to fetch data.
5. The view passes that data into a **template** via `render()`.
6. The **template** renders HTML using DTL tags/filters, referencing static files (CSS/JS) as needed.
7. Django returns the final HTML as an `HttpResponse` to the browser.

```
Browser → urls.py → views.py → models.py (DB) → templates/*.html → HttpResponse → Browser
```

This request/response cycle, combined with Models–Views–Templates, is the entire mental model you need to build any Django feature.