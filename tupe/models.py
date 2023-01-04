from django.db import models
from django.urls import reverse


class Tupe(models.Model):
    class Meta:
        verbose_name = 'Вышивка одежды'
        verbose_name_plural = 'Вышивка одежды'
        ordering = ['time_create', 'title']
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name='Текст')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/",verbose_name='Фоточки',null=True, blank=True)
    time_create = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    time_update = models.DateTimeField(auto_now=True, verbose_name='Текст', null=True, blank=True)
    is_published = models.BooleanField(default=True, null=True, blank=True)
    cat = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})#маршрут по url


class Category(models.Model):
    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug}) #маршрут по url
