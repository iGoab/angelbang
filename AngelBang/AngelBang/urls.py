"""AngelBang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog.feeds import AllPostsRssFeed
from markdownx import urls as markdownx
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('angelbang/', admin.site.urls),
    path('', include('blog.urls')),
    path('comment/', include('comments.urls')),
    path('all/rss/', AllPostsRssFeed(), name='rss'),
    path('search', include('haystack.urls')),
    path('markdownx/', include(markdownx)),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]

# 添加图片url解析
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)