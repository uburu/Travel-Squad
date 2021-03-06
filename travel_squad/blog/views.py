from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import JsonResponse
from .models import Article, Photos, Tags
from .forms import SearchForm
from .utils import getParamURL


def _paginate(objects_list, request, page=None):
    objects_page = []

    if not page:
        page = request.GET.get('page')

    paginator = Paginator(objects_list, 12)

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


def index(request):
    all_posts = _paginate(Article.objects.all_articles(), request)
    first_half = all_posts[:4]

    tags = Tags.objects.all_tags()
    context = {
        'columns': first_half,
        'all_posts': all_posts,
        'tags': tags
    }
    return render(request, 'index.html', context)


def gallery(request):
    all_photos = _paginate(Photos.objects.all_photos(), request)
    row1 = all_photos[:3]
    row2 = all_photos[3:6]
    row3 = all_photos[6:9]
    row4 = all_photos[9:12]

    tags = Tags.objects.all_tags()

    context = {
        'all_photos': all_photos,
        'row_1': row1,
        'row_2': row2,
        'row_3': row3,
        'row_4': row4,
        'last_query': '',
        'tags': tags
    }

    return render(request, 'gallery.html', context)


def stories(request):
    all_stories = _paginate(Article.objects.all_articles(), request)
    tags = Tags.objects.all_tags()

    stories1 = all_stories[:3]
    stories2 = all_stories[3:6]
    stories3 = all_stories[6:9]
    stories4 = all_stories[9:12]
    stories5 = all_stories[12:15]

    context = {
        'all_stories': all_stories,
        'stories_1': stories1,
        'stories_2': stories2,
        'stories_3': stories3,
        'stories_4': stories4,
        'stories_5': stories5,
        'last_query': '',
        'tags': tags
    }
    return render(request, 'stories.html', context)


def about(request):
    return render(request, 'aboutus.html')


def photos_by_tag(request, tag_name):
    photos_by_tag = _paginate(Photos.objects.all_photos_by_tag(tag_name), request)

    row1 = photos_by_tag[:3]
    row2 = photos_by_tag[3:6]
    row3 = photos_by_tag[6:9]
    row4 = photos_by_tag[9:12]

    tags = Tags.objects.all_tags()

    context = {
        'all_photos': photos_by_tag,
        'row_1': row1,
        'row_2': row2,
        'row_3': row3,
        'row_4': row4,
        'last_query': '',
        'tags': tags
    }
    return render(request, 'gallery.html', context)


def photo(request, id):
    photo_by_id = Photos.objects.get_photo_by_id(id)
    print(photo_by_id)

    return render(request, 'photo.html', {'photo': photo_by_id})


def stories_by_tag(request, tag_name):
    all_stories = _paginate(Article.objects.all_articles_by_tag(tag_name), request)
    tags = Tags.objects.all_tags()

    stories1 = all_stories[:3]
    stories2 = all_stories[3:6]
    stories3 = all_stories[6:9]
    stories4 = all_stories[9:12]
    stories5 = all_stories[12:15]

    context = {
        'all_stories': all_stories,
        'stories_1': stories1,
        'stories_2': stories2,
        'stories_3': stories3,
        'stories_4': stories4,
        'stories_5': stories5,
        'last_query': '',
        'tags': tags
    }
    return render(request, 'stories.html', context)


# TODO если зайти в конкретный пост, а потом попытаться выйти из него нажатием стрелочки назад в браузере, то на экран вылезает весь текст предыдущего ajax запроса
# кнопка назад вообще не работает с ajax запросами, и в пагинации тоже - разобраться
def post(request, id):
    article = get_object_or_404(Article, pk=id)
    photos = Photos.objects.get_photo_by_post(article)
    context = {
        'post': article,
        'photos': photos
    }
    return render(request, 'post.html', context)


def search_results(request):
    search_form = SearchForm()
    last_query = ''
    if request.method == 'GET':
        search_form = SearchForm(request.GET)
        if search_form.is_valid():

            # TODO подумать над необходимостью формы, мб ее лучше убрать
            keywords = getParamURL(request.get_full_path(), 'query')
            page = getParamURL(request.get_full_path(), 'page')

            if keywords:  # если поисковой запрос не пустой

                last_query = '?query=%s/' % keywords  # формирование строки URL для корректной работы пагинации
                results_of_searching = Article.objects.all_articles()
                query = SearchQuery(keywords)
                title_vector = SearchVector('title', weight='A')
                text_vector = SearchVector('text', weight='B')
                vectors = title_vector + text_vector
                results_of_searching = results_of_searching.annotate(search=vectors).filter(search=query)
                results_of_searching = results_of_searching.annotate(rank=SearchRank(vectors, query)).order_by('-rank')
                results_of_searching = _paginate(results_of_searching, request, page)

            return view_body(request, results_of_searching, last_query)
