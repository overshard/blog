from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.core import hooks


@hooks.register("insert_editor_js", order=100)
def global_admin_js():
    return format_html('<script src="{}"></script>', static("admin.js"))


@hooks.register("insert_editor_css", order=100)
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("admin.css"))
