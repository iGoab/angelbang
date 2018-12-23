from django.contrib import admin
from django.db import models
from .models import Post, Category,Tag,Catalog
from markdownx.widgets import AdminMarkdownxWidget

@admin.register(Post)
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_deleted', 'created_time', 'modified_time','views', 'likes')
    exclude = ['views', 'likes']
    formfield_overrides = {
        models.TextField:{'widget':AdminMarkdownxWidget},
    }

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Catalog)