from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.core import hooks
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin

from pages.models import BlogPostPage


@hooks.register("insert_editor_js", order=100)
def global_admin_js():
    return format_html('<script src="{}"></script>', static("admin.js"))


@hooks.register("insert_editor_css", order=100)
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("admin.css"))


class BlogPostPageAdmin(ThumbnailMixin, ModelAdmin):
    model = BlogPostPage
    menu_label = 'Posts'
    menu_icon = 'doc-full-inverse'
    exclude_from_explorer = True
    menu_order = 200
    list_display = ('admin_thumb', 'title', 'first_published_at', 'tags_list')
    list_filter = ('tags',)
    search_fields = ('title', 'body')
    ordering = ('-first_published_at',)
    thumb_image_field_name = 'cover_image'
    thumb_image_width = 100

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tags_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())


modeladmin_register(BlogPostPageAdmin)
