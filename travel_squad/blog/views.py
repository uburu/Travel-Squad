from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.csrf import requires_csrf_token

from django.http import JsonResponse
from .models import Article, Photos, Tags

# Create your views here.


def _paginate(objects_list, request):
    objects_page = []

    paginator = Paginator(objects_list, 4)
    page = request.GET.get('page')
    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        objects_page = paginator.page(1)
    except EmptyPage:
        page = int(page)
        if page < 1:
            objects_page = paginator.page(1)
        elif page > paginator.num_pages:
            objects_page = paginator.page(paginator.num_pages)
    return objects_page


# def index(request):
#     all_posts = _paginate(Article.objects.all_new(), request)
#     first_half = all_posts[:2]
#     second_half = all_posts[2:]  # посмотреть что будет при пустом list []

#     context = {
#         'left_column': first_half,
#         'right_column': second_half,
#         'all_posts': all_posts
#     }
#     return render(request, 'index.html', context)

# def _sidebar_context():
#     return {
#         'tags': Tags.objects.all_tags()
#     }


@requires_csrf_token
def index(request):
    all_posts = _paginate(Article.objects.all_new(), request)
    first_half = all_posts[:2]
    second_half = all_posts[2:]

    tags = Tags.objects.all_tags()
    if request.method == 'GET':
        context = {
            'left_column': first_half,
            'right_column': second_half,
            'all_posts': all_posts,
            'tags': tags
        }
        return render(request, 'index.html', context)

    if request.method == 'POST':
        if request.is_ajax():
            cont = {
                'left_column': first_half,
                'right_column': second_half,
                'all_posts': all_posts,
                'tags': tags
            }
            return JsonResponse({
                'result': True,
                'articles': render_to_string(
                    request=request,
                    template_name='_shortArticles_list.html',
                    context=cont
                )
            })
        else:
            raise Http404('page does not exist')


def articles_by_tag(request, tag):
    if request.method == 'GET':
        articles_by_tag = _paginate(Article.objects.all_articles_by_tag(tag), request)
        first_half = articles_by_tag[:2]
        second_half = articles_by_tag[2:]

        tags = Tags.objects.all_tags()
        cont = {
            'left_column': first_half,
            'right_column': second_half,
            'all_posts': articles_by_tag,
            'tags': tags
        }
        if request.is_ajax():
            return JsonResponse({
                'result': True,
                'articles': render_to_string(
                    request=request,
                    template_name='_shortArticles_list.html',
                    context=cont
                    )
                })
        else:
            raise Http404('page does not exist')
    else:
        raise Http404('page does not exist')


def post(request, id):
    article = get_object_or_404(Article, pk=id)
    context = {
        'post': article
    }
    return render(request, 'post.html', context)
