from wagtail import hooks
from wagtail.admin.menu import MenuItem


@hooks.register("register_admin_menu_item")
def register_menu_item():
    return MenuItem(
        "Wagtail Heelo World",
        "/admin/wagtail_heelo_world/",
        icon_name="cog",
        order=10000,
    )


# Uncomment to add custom admin URLs
# @hooks.register("register_admin_urls")
# def register_admin_urls():
#     from django.urls import path
#     from . import views
#     return [
#         path("wagtail_heelo_world/", views.index, name="wagtail_heelo_world_index"),
#     ]
