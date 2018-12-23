from django.contrib import admin
from .models import Comments
# Register your models here.

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'user', 'text', 'created_time', 'is_deleted' )