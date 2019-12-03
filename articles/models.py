from django.db import models
from ckeditor.fields import RichTextField

from pytils.translit import slugify
from django.core.mail import EmailMessage
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    short_description = models.TextField(max_length=134, verbose_name='Описание статьи')
    description = RichTextField(verbose_name='Текст статьи')
    time_for_read = models.IntegerField(verbose_name='Время на чтение', blank=True, null=True)
    category = models.ManyToManyField('ArticleCategory', verbose_name='Категория')
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение')
    author = models.ForeignKey('ArticleAuthor', on_delete=models.PROTECT, verbose_name='Автор')
    article_pdf = models.FileField(null=True, blank=True, verbose_name='Статья в pdf')

    def sent_file_in_mail(self, client, request):
        media_root = settings.MEDIA_ROOT
        domain = request.META['HTTP_HOST']
        message = EmailMessage(subject='Статья с сайта %s' % domain,
                               body='Вам понравилась статья %s на сайте %s. Чтобы не потерять, высылаем ее в удобном формате' % (self.title, domain),
                               to=[client.email],
                               from_email=settings.EMAIL_HOST_USER if settings.DEBUG else None)
        message.attach_file('%s/%s' % (media_root, self.article_pdf))
        return message.send()

    def save(self, *args, **kwargs):
        super(Article, self).save()
        if not self.slug.endswith('-' + str(self.id)):
            self.slug += '-' + str(self.id)
        super(Article, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class ArticleCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название категории')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ArticleAuthor(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    position = models.CharField(max_length=200, verbose_name='Должность')
    image = models.ImageField(blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return '%s - %s' % (self.name, self.position)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


