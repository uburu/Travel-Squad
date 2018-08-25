from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Article, Tags, Photos
from faker import Faker
import random

photos = ['photos/1.jpg', 'photos/2.jpg', 'photos/3.jpg', 'photos/4.jpg',
          'photos/5.jpg', 'photos/6.jpg', 'photos/7.jpg', 'photos/8.jpg']


class Command(BaseCommand):

    help = 'This command fills existing tables in your data base'

    def handle(self, *args, **options):
        self.create_admin()
        self.fill_tags()
        self.fill_articles()
        self.stdout.write(self.style.SUCCESS('Finish to fill the database'))

    def create_admin(self):
        # если нет этой проверки то после первого запуска скрипта будет вылезать
        # ошибка UNIQUE constraint failed: auth_user.username django - пользователь с таким именем уже есть
        if User.objects.count() > 0:
            return
        User.objects.create_superuser(username='admin', password='qwerty1234', email='e@mail.ru')

    def fill_articles(self):
        if Article.objects.count() > 0:
            return

        fake = Faker()
        tags_set = Tags.objects.all()
        print()
        for i in range(40):
            post = Article()
            post.title = fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
            post.text = fake.text(max_nb_chars=3000, ext_word_list=None)
            post.creationDate = fake.date(pattern="%Y-%m-%d", end_datetime=None)
            post.departureDate = fake.date(pattern="%Y-%m-%d", end_datetime=None)
            post.returnDate = fake.date(pattern="%Y-%m-%d", end_datetime=None)
            post.shortDescription = fake.text(max_nb_chars=700, ext_word_list=None)
            post.image = random.choice(photos)
            post.id = i
            post.save()

            # заполениение поля ManyToManyField() должно происходить после сохранения записи в базу (после post.save())
            # иначе будет  instance is on database "None", value is on database "default" - невозможно связать с несуществующей записью

            for j in range(3):
                t = random.choice(tags_set)
                post.tags.add(t)
                self.stdout.write('add tag [%s] in article [%d]' % (t, i))

            self.stdout.write('add article [%d]' % post.id)

    def fill_tags(self):
        if Tags.objects.count() > 0:
            return
        fake = Faker()
        random_tags = fake.words(nb=10, ext_word_list=None)
        for tag in random_tags:
            t = Tags()
            t.name = tag
            t.save()
            self.stdout.write('add tag [%s]' % tag)


    def fill_photos(self):
        pass
