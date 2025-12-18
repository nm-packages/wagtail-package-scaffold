from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class WagtailHeeloWorldPage(Page):
    """
    Example page model - customize or replace as needed.
    """

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Wagtail Heelo World Page"
        verbose_name_plural = "Wagtail Heelo World Pages"
