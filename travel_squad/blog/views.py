from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import JsonResponse
from .models import Article, Photos, Tags
from .forms import SearchForm
from .utils import getParamURL


# Create your views here.



# def index(request):
#     all_posts = _paginate(Article.objects.all_articles(), request)
#     first_half = all_posts[:2]
#     second_half = all_posts[2:]  # посмотреть что будет при пустом list []

#     tags = Tags.objects.all_tags()
#     context = {
#         'left_column': first_half,
#         'right_column': second_half,
#         'all_posts': all_posts,
#         'tags': tags
#     }
#     return render(request, 'index.html', context)


# @requires_csrf_token
# def articles_by_tag(request, tag_name):
#     all_posts = _paginate(Article.objects.all_articles_by_tag(tag_name), request)
#     first_half = all_posts[:2]
#     second_half = all_posts[2:]

#     tags = Tags.objects.all_tags()
#     context = {
#         'left_column': first_half,
#         'right_column': second_half,
#         'all_posts': all_posts,
#         'tags': tags
#     }
#     return render(request, 'index.html', context)

def _paginate(objects_list, request, page=None):
    objects_page = []

    if not page:
        page = request.GET.get('page')

    paginator = Paginator(objects_list, 4)

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


def view_body(request, all_posts, last_query=''):
    first_fourth = all_posts[:4]
    # second_half = all_posts[2:]

    tags = Tags.objects.all_tags()

    search_form = SearchForm(request.GET)
    context = {
        'columns': first_fourth,
        'all_posts': all_posts,
        'tags': tags,
        'form': search_form,
        'last_query': last_query
    }

    if request.method == 'GET':
        if request.is_ajax():
            return JsonResponse({
                'result': True,
                'articles': render_to_string(
                    request=request,
                    template_name='_shortArticles_list.html',
                    context=context
                    )
                })
        else:
            return render(request, 'index.html', context)
    else:
        raise Http404('page does not exist')

def index(request):
    all_posts = _paginate(Article.objects.all_articles(), request)

    if len(all_posts) > 0:
        return view_body(request, all_posts)
    else:
        raise Http404()


def articles_by_tag(request, tag_name):
    articles_by_tag = _paginate(Article.objects.all_articles_by_tag(tag_name), request)

    if len(articles_by_tag) > 0:
        return view_body(request, articles_by_tag)
    else: # сейчас выпадает 404 если ввести несуществующий tag в адресную строку, но вообще хорошо бы показать какую-нибудь страничку
        raise Http404()


#TODO если зайти в конкретный пост, а потом попытаться выйти из него нажатием стрелочки назад в браузере, то на экран вылезает весь текст предыдущего ajax запроса
# кнопка назад вообще не работает с ajax запросами, и в пагинации тоже - разобраться
def post(request, id):
    article = get_object_or_404(Article, pk=id)
    context = {
        'post': article
    }
    return render(request, 'post.html', context)


def search_results(request):
    search_form = SearchForm()
    last_query = ''
    if request.method == 'GET':
        search_form = SearchForm(request.GET)
        if search_form.is_valid():

            #TODO подумать над необходимостью формы, мб ее лучше убрать
            keywords = getParamURL(request.get_full_path(), 'query')
            page = getParamURL(request.get_full_path(), 'page')

            if keywords: # если поисковой запрос не пустой

                last_query = '?query=%s/' % keywords # формирование строки URL для корректной работы пагинации
                results_of_searching = Article.objects.all_articles()
                query = SearchQuery(keywords)
                title_vector = SearchVector('title', weight='A')
                text_vector = SearchVector('text', weight='B')
                vectors = title_vector + text_vector
                results_of_searching = results_of_searching.annotate(search=vectors).filter(search=query)
                results_of_searching = results_of_searching.annotate(rank=SearchRank(vectors, query)).order_by('-rank')
                results_of_searching = _paginate(results_of_searching, request, page)
            
            return view_body(request, results_of_searching, last_query)

