from django import template
from ..models import Post,Category, Tag, Catalog
from django.db.models import Count
register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.filter(is_deleted=False).order_by('-created_time')[:num]


@register.simple_tag
def archives():
    return Post.objects.filter(is_deleted=False).dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.filter(post__is_deleted=False).annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_hot_posts(num=5):
    return Post.objects.filter(is_deleted=False).order_by('-likes')[:num]


@register.simple_tag
def get_catalogs():
    return Catalog.objects.all().order_by('id')