from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('tag/<slug:tag_name>', views.articles_by_tag, name='articles_by_tag'),
    path('post/<int:id>', views.post, name='post'),
    path('search/', views.search_results, name='search_results'),
    path('gallery/', views.gallery, name='gallery'),
    path('phototag/<slug:tag_name>', views.photos_by_tag, name='photos_by_tag'),
    path('stories/', views.stories, name='stories'),
    path('storytag/<slug:tag_name>', views.stories_by_tag, name='stories_by_tag'),
    path('about/', views.about, name='about')
]
