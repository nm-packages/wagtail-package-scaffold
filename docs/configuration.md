# Configuration

## Django Settings

### Basic Configuration

Add the following to your Django settings file:

```python
# Required: Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    "wagtail_heelo_world",
    # ...
]
```

### Optional Settings

You can customize the package behavior with these settings:

```python
# Example optional settings - customize as needed
WAGTAIL_HEELO_WORLD_SETTING = "value"
```

## Using the Page Model

The package includes an example page model `WagtailHeeloWorldPage` that you can use:

```python
from wagtail_heelo_world.models import WagtailHeeloWorldPage

# The page model includes:
# - A RichTextField for body content
# - Standard Wagtail Page fields
# - Admin panel configuration
```

### Creating Pages Programmatically

```python
from wagtail.models import Site
from wagtail_heelo_world.models import WagtailHeeloWorldPage

# Get the site root page
site = Site.objects.get(is_default_site=True)
root_page = site.root_page

# Create a new page
new_page = WagtailHeeloWorldPage(
    title="My Hello World Page",
    slug="hello-world",
    body="<p>Welcome to my page!</p>",
)
root_page.add_child(instance=new_page)
```

## Admin Customization

The package registers a menu item in the Wagtail admin. You can customize this by:

1. Editing `wagtail_hooks.py` in your local installation
2. Adjusting the icon, order, and URL as needed

## Templates

Override the default templates by creating your own in:

```
your_project/templates/wagtail_heelo_world/
```

## Static Files

Custom static files should be placed in:

```
your_project/static/wagtail_heelo_world/
```

## Advanced Configuration

For more advanced customization, consider:

- Subclassing the provided models
- Creating custom Wagtail hooks
- Adding custom admin views
- Extending templates

## Environment Variables

For production deployments, consider using environment variables:

```python
import os

WAGTAIL_HEELO_WORLD_SETTING = os.getenv(
    "WAGTAIL_HEELO_WORLD_SETTING",
    "default_value"
)
```

## Next Steps

- Explore the source code in `src/wagtail_heelo_world/`
- Check out the sandbox site for examples
- Read the [Wagtail documentation](https://docs.wagtail.org/) for more on customization
