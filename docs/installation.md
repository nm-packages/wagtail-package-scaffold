# Installation

## Requirements

Before installing wagtail-heelo-world, ensure you have:

- Python 3.10 or higher
- Django 4.2 or higher
- Wagtail 6.0 or higher

## Installation Steps

### 1. Install the package

```bash
pip install wagtail-heelo-world
```

### 2. Add to INSTALLED_APPS

Add `wagtail_heelo_world` to your Django settings:

```python
INSTALLED_APPS = [
    # ...
    "wagtail_heelo_world",
    # ...
]
```

Place it after the Wagtail apps but before your own apps.

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Collect static files

```bash
python manage.py collectstatic
```

## Verification

To verify the installation:

1. Start your development server
2. Log into the Wagtail admin
3. Look for "Wagtail Heelo World" in the admin menu

## Troubleshooting

### Package not found

If you get an import error, ensure the package is installed in your active virtual environment:

```bash
pip list | grep wagtail-heelo-world
```

### Admin menu item not appearing

Make sure you've:
1. Added the app to `INSTALLED_APPS`
2. Restarted your development server
3. Cleared your browser cache

## Next Steps

See [Configuration](configuration.md) for customization options.
