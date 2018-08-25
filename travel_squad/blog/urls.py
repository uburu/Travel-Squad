from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<slug:tag_name>', views.articles_by_tag, name='articles_by_tag'),
    path('post/<int:id>', views.post, name='post'),
    path('search/', views.search_results, name='search_results')
]
