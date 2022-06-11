from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.blocks import (ChoiceBlock, RichTextBlock, StructBlock,
                                 TextBlock)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

from .utils import og_image


class StreamPageAbstract(Page):
    body = StreamField(
        [
            ('rich_text', RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('code', StructBlock([
                ('language', ChoiceBlock(choices=[
                    ('python', 'Python'),
                    ('javascript', 'Javascript'),
                    ('htmlmixed', 'HTML'),
                    ('css', 'CSS'),
                    ('shell', 'Shell'),
                ])),
                ('text', TextBlock()),
            ])),
            ('embed', EmbedBlock()),
        ],
        use_json_field=True,
        blank=True,
    )
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Cover image for this page, used in listings and at the top of the page.'
    )

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('cover_image'),
    ]
    promote_panels.pop(1)  # Remove the 'For site menus' item

    settings_panels = Page.settings_panels + [
        FieldPanel('first_published_at'),
    ]

    search_feilds = Page.search_fields + [
        index.SearchField('body'),
    ]

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super_save = super().save(*args, **kwargs)
        og_image(self.full_url, force=True)
        return super_save


class HomePage(StreamPageAbstract):
    max_count = 1

    page_description = "The home of our website, you should only have one of these"

    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['BlogIndexPage', 'SearchPage']

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Pages'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['latest_post'] = BlogPostPage.objects.live().public().order_by('-first_published_at').first()
        context['random_blog_posts'] = BlogPostPage.objects.live().public().order_by('?')[:3]
        return context


class SearchPage(RoutablePageMixin, StreamPageAbstract):
    max_count = 1

    page_description = "The search page of our website, you should only have one of these"

    parent_page_types = ['HomePage']
    subpage_types = []

    class Meta:
        verbose_name = 'Search Page'
        verbose_name_plural = 'Search Pages'

    @route(r'^$')
    def search(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        results = BlogPostPage.objects.live().public().search(q)
        # combine live search results too just incase the user hits enter
        # instead of clicking a result
        results = list(results) + list(BlogPostPage.objects.live().public().filter(
            Q(title__icontains=q) | Q(search_description__icontains=q) | Q(tags__name__icontains=q)
        ).exclude(id__in=[r.id for r in results]).distinct()[:5])
        return self.render(request, context_overrides={'results': results})

    @route(r'^live/$')
    def live_search(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        # NOTE: wagtail's autocomplete feature doesn't work with sqlite so I'm
        # doing a bit of a workaround, you should use autocomplete if you can
        results_queryset = BlogPostPage.objects.live().public().filter(
            Q(title__icontains=q) | Q(search_description__icontains=q) | Q(tags__name__icontains=q)
        ).distinct()[:5]
        results = []
        for result in results_queryset:
            results.append({
                'title': result.title,
                'description': result.search_description,
                'url': result.full_url,
            })
        return JsonResponse(results, safe=False)


class BlogIndexPage(RoutablePageMixin, StreamPageAbstract):
    max_count = 1

    page_description = "For showing our blog posts and allowing filtering, you should only have one of these"

    parent_page_types = ['HomePage']
    subpage_types = ['BlogPostPage']

    class Meta:
        verbose_name = 'Blog Index Page'
        verbose_name_plural = 'Blog Index Pages'

    def get_blog_posts(self):
        return BlogPostPage.objects.live().public().order_by('-first_published_at')

    def get_tags(self):
        tag_ids = list(set(BlogPostPage.objects.live().public().values_list('tags', flat=True)))
        return Tag.objects.filter(id__in=tag_ids)

    def get_years(self):
        return list(set(BlogPostPage.objects.live().public().values_list('first_published_at__year', flat=True)))

    @route(r'^$')
    def index(self, request):
        blog_posts = self.get_blog_posts()
        return self.render(request, context_overrides={'blog_posts': blog_posts})

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def tag(self, request, tag):
        blog_posts = self.get_blog_posts().filter(tags__slug=tag)
        active_tag = Tag.objects.get(slug=tag)
        return self.render(request, context_overrides={'blog_posts': blog_posts, 'active_tag': active_tag})

    @route(r'^year/(?P<year>\d+)/$')
    def year(self, request, year):
        blog_posts = self.get_blog_posts().filter(first_published_at__year=year)
        return self.render(request, context_overrides={'blog_posts': blog_posts})

    def get_sitemap_urls(self, request=None):
        # add original url
        urls = [
            {
                "location": self.get_full_url(request),
                "lastmod": self.last_published_at,
            }
        ]
        # add tag urls
        for tag in self.get_tags():
            urls.append({
                "location": self.get_full_url(request) + self.reverse_subpage('tag', kwargs={'tag': tag.slug}),
                "lastmod": self.last_published_at,
            })
        # add year urls
        for year in self.get_years():
            urls.append({
                "location": self.get_full_url(request) + self.reverse_subpage('year', kwargs={'year': year}),
                "lastmod": self.last_published_at,
            })
        return urls


class BlogPostPageTags(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPostPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BlogPostPage(StreamPageAbstract):
    tags = ClusterTaggableManager(through=BlogPostPageTags, blank=True)

    promote_panels = StreamPageAbstract.promote_panels + [
        FieldPanel('tags'),
    ]

    page_description = "For the majority of our blog posts"

    parent_page_types = ['BlogIndexPage']
    subpage_types = []

    class Meta:
        verbose_name = "Blog Page"
        verbose_name_plural = "Blog Pages"
        ordering = ['-first_published_at']
