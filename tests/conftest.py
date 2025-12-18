import pytest
from django.conf import settings


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }


@pytest.fixture
def sample_data():
    """Provide sample test data."""
    return {
        "title": "Test Title",
        "body": "<p>Test content</p>",
    }
