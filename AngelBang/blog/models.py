from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from markdownx.models import MarkdownxField
import markdown
from AngelBang.settings import(
    MARKDOWNX_MARKDOWN_EXTENSIONS,
    MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
)
from django.utils.html import strip_tags

class Catalog(models.Model):
    """
    目录
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    分类
    """
    name = models.CharField(max_length=100)
    catalog = models.ForeignKey(Catalog, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Post(models.Model):
    """
    文章
    """
    # 标题
    title = models.CharField(max_length=70)

    # 正文
    body = models.TextField()
    # 摘要
    excerpt = models.CharField(max_length=200, blank=True)

    # 创建时间
    created_time = models.DateTimeField(auto_now_add=True)

    # 修改时间
    modified_time = models.DateTimeField(auto_now=True)

    # 分类
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    # 标签
    tags = models.ManyToManyField(Tag, blank=True)

    # 阅读量
    views = models.PositiveIntegerField(default = 0)

    # 喜欢量
    likes = models.PositiveIntegerField(default=0)

    # 作者
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    # 是否删除
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def update_likes(self, likes):
        self.likes = likes
        self.save(update_fields=['likes'])

    def word_count(self):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # TODO: refactor and test
        return len(strip_tags(md.convert(self.body)))
        
    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=MARKDOWNX_MARKDOWN_EXTENSIONS,
                                extensions_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS)
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super(Post, self).save(*args, **kwargs)


    class Meta:
        ordering = ['-created_time']