from django.db import models

# Create your models here.


class Post(models.Model):

    class Meta:
        db_table = 'post'  # название таблицы
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        ordering = ['creationDate']

    title = models.CharField('Название статьи', max_length=256)
    text = models.TextField('Текст статьи')
    creationDate = models.DateField(auto_now_add=True)
    images = models.ImageField(upload_to='photos', default='static/img/logo_black.png')

    def __str__(self):
        return self.title


class Photos(models.Model):

    class Meta:
        db_table = 'photos'
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    photo = models.ImageField('Фотография', default=None)

    def __str__(self):
        return 'фото к статье ' + '"' + self.post.title + '"'


