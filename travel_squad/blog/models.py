from django.db import models
from django.contrib.postgres.search import SearchVectorField

# Create your models here.


class TagsManager(models.Manager):
    def all_tags(self):
        return self.all()


class Tags(models.Model):

    class Meta:
        db_table = 'tags'
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    objects = TagsManager()
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ArticleManager(models.Manager):
    def all_articles(self):
        return self.all()

    def all_articles_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)


class Article(models.Model):

    class Meta:
        db_table = 'post'  # название таблицы
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        ordering = ['creationDate']

    objects = ArticleManager()
    title = models.CharField('Название статьи', max_length=256)
    text = models.TextField('Текст статьи', default=None)
    shortDescription = models.TextField('Краткое описание', default=None)
    creationDate = models.DateField(auto_now_add=True) # дата создания поста
    image = models.ImageField('Титульная фотография', upload_to='photos/', default=None) # если будет одна фотка в посте то ее удобнее добавлять сразу со страницы поста
    departureDate = models.DateField('Дата начала путешествия', default=None)
    returnDate = models.DateField('Дата окончания путешествия', default=None)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.title



class PhotosManager(models.Manager):
    def all_photos(self):
        return self.all()
    def all_photos_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)



class Photos(models.Model):

    class Meta:
        db_table = 'photos'
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

    objects = PhotosManager()
    post = models.ForeignKey(Article, on_delete=models.CASCADE, default=None)
    img = models.ImageField('Фотография', upload_to='photos/', default=None)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return 'фото к статье ' + '"' + self.post.title + '"'