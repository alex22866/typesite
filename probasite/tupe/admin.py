from django.contrib import admin

from tupe.models import *


class TupeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')  # содержит список полей которых хотим видят в админ панели
    list_display_links = ('id', 'title')  # поля на которые мы переходим
    search_fields = ('title', 'content')  # поиск по полям
    list_editable = ['is_published']#галочки в адм панель публикация статьи
    list_filter = ['is_published']#фильт сбоку адм панели
    prepopulated_fields = {"slug": ("title",)}#заполняет автомат поле на основе текста(title,name)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # содержит список полей которых хотим видят в админ панели
    list_display_links = ('id', 'name')  # поля на которые мы переходим
    search_fields = ('name',)  # поиск по полям
    prepopulated_fields = {"slug": ("name",)}#заполняет автомат поле на основе name


admin.site.register(Tupe, TupeAdmin)
admin.site.register(Category, CategoryAdmin)
