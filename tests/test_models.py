import pytest

from wagtail_heelo_world.models import WagtailHeeloWorldPage


@pytest.mark.django_db
class TestWagtailHeeloWorldPage:
    def test_can_create_page(self, django_db_setup):
        """Test that the page model can be instantiated."""
        page = WagtailHeeloWorldPage(
            title="Test Page",
            slug="test-page",
            body="<p>Test content</p>",
        )
        assert page.title == "Test Page"
        assert page.body == "<p>Test content</p>"

    def test_page_verbose_name(self):
        """Test the model's verbose name."""
        assert WagtailHeeloWorldPage._meta.verbose_name == "Wagtail Heelo World Page"
