from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/id=<int:id>', views.read),
    path('write/', views.write),
    path('delete/id=<int:id>', views.delete),
    path('edit/id=<int:id>', views.edit),
    path('like/', views.like_blog , name='like_post'),
]
                  