from django.db import models
from django.conf import settings

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock


class BlogIndexPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        tag = request.GET.get('tag')
        if tag is not None:
            blogpages = blogpages.filter(blogpage__tags__name=tag)
        context['blogpages'] = blogpages
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True, null=True,
        verbose_name='Author',
        on_delete=models.SET_NULL,
        related_name='author_pages',
    )
    date = models.DateField("Post date")
    intro = models.CharField(max_length=511, null=True, blank=True)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    body = StreamField([
        (
            'heading',
            blocks.CharBlock(
                classname="full title",
                template='blog/heading.html',
            )
        ),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('author'),
                FieldPanel('date'),
                FieldPanel('tags'),
            ],
            heading="Blog information"
        ),
        StreamFieldPanel('body'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]


class BlogAboutPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

