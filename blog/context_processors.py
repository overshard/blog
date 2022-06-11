from django.conf import settings
from taggit.models import Tag
from pages.models import BlogIndexPage


def canonical(request):
    """
    Gets the canonical URL for the current request.
    """
    return {"canonical": request.build_absolute_uri(request.path)}


def base_url(request):
    """
    Provides the BASE_URL from settings.
    """
    return {"BASE_URL": settings.BASE_URL}


def nav_items(request):
    """
    Provides tags for the navigation.
    """
    blog_index_page = BlogIndexPage.objects.first()
    if blog_index_page:
        tags = blog_index_page.get_tags()
    else:
        tags = Tag.objects.none()
    for tag in tags:
        tag.name = tag.name.title()
        tag.url = blog_index_page.url + blog_index_page.reverse_subpage(
            'tag', kwargs={'tag': tag.slug}
        )
    sorted_tags = sorted(tags, key=lambda tag: tag.name)
    return {"nav_items": sorted_tags}
