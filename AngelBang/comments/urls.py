from django.urls import path

from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/', views.update_comments, name = 'update_comments'),
]