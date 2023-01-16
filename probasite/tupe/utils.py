from django.db.models import Count

from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'addpage'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]

#чтобы не дублировался код(общий код)
class DataMixin:
    paginate_by = 20  #пагинация (цифра показывет сколько будет показ катег
    def get_user_context(self, **kwargs):#формирует нудный контекст по умол
        context = kwargs        #формируем начальный словарь
        cats = Category.objects.annotate(Count('tupe')) #выбирает категории

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context