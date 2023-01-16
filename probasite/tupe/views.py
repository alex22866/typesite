from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *



'''пример пагинации с классом'''
#класс представления
#DataMixin без дублирования

class TupeHome(DataMixin, ListView):
    #убираем дубликацию в DataMixin
    # paginate_by = 3 #пагинация (цифра показывет сколько будет показ катег

    model = Tupe  #подкл к модели
    template_name = 'tupe/index.html' #подк к шаблону
    context_object_name = 'posts'  #подл к шаблону индекс


    #функция передает параметры context
    def get_context_data(self, *, object_list=None, **kwargs): #формуриет динамич и статический контекст
        context = super().get_context_data(**kwargs) #формированные контекста существующий
        c_def = self.get_user_context(title='Главная страница')#
        return dict(list(context.items()) + list(c_def.items())) #возращает словарь


    #метод который показывает те катег которые выбраныя категории
    def get_queryset(self):
        return Tupe.objects.filter(is_published=True)#фильтрует только опубликованные записи из за is_published


#
# def index(request):
#     posts = Tupe.objects.all()
#     params = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'tupe/index.html', params)

'''пример пагинации с функцией'''
def about(request):
    contact_list = Tupe.objects.all()   #выводит список катег
    paginator = Paginator(contact_list, 5) #пагинация (указанная цифрапоказываает сколько будетстатей
    page_number = request.GET.get('page')   #номер текущей стр из GET запроса
    page_obj = paginator.get_page(page_number) #содерж список эдемент текущ стр
    params = {
        'menu': menu,
        'title': 'О сайте',
        'page_obj': page_obj,
    }
    return render(request, 'tupe/about.html', params)


#работа с формами CreateView
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'tupe/addpage.html' #ссылка на шаблон
    login_url = reverse_lazy ('home')#не зарег пользователь перенапр в админку
    success_url = reverse_lazy('home')#если форма успешна заполнена то будет перенаправ на гл стр
    raise_exception = True #403 доступ запрещен

    # функция передает параметры context
    def get_context_data(self, *, object_list=None, **kwargs):  # формуриет динамич и статический контекст
        context = super().get_context_data(**kwargs)  # формированные контекста существующий
        c_def = self.get_user_context(title='Добавление статьи')#
        return dict(list(context.items()) + list(c_def.items())) #возращает словарь



# def addpage(request):
#     if request.method == 'POST':        #проверка полей заполнены ли они
#         form = AddPostForm(request.POST, request.FILES) #заполненные данных, request.FILES - для фоток
#         if form.is_valid(): #корректны ли были заполнены данные
#         # print(form.cleaned_data)
#             form.save() #сохр в бд
#             return redirect('home')#переход на гл страницу
#     else:
#         form = AddPostForm() #формируется пустая форма
#     params = {
#         "form": form,
#         "menu": menu,
#         "title": 'Главная страница',
#     }
#     return render(request, 'tupe/addpage.html', params)



#FormView - стандартный класс который не привязан к бд
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm    #ссылка на форму ContactForm
    template_name = 'tupe/contact.html'     #шаблон
    success_url = reverse_lazy('home')      #если форма успешно заполнена то будет перенаправ на гл стр

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))


#dsвызывается в случае если верно заполнил все поля формы
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


# def login(request):
#     return HttpResponse("login")


#класс для постов DetailView
class ShowPost(DataMixin, DetailView):
    model = Tupe
    template_name = 'tupe/post.html'    #ссылка на шаблон
    slug_url_kwarg = 'post_slug' #маршутизация для слага без ошибок
    # pk_url_kwarg - для id
    context_object_name = 'post' #для отображения в шаблоне post(подл к шаблону)


    # функция формирует динамич контекст
    def get_context_data(self, *, object_list=None, **kwargs):  # формуриет динамич и статический контекст
        context = super().get_context_data(**kwargs)  # формированные контекста существующий
        c_def = self.get_user_context(title=context['post'])#
        return dict(list(context.items()) + list(c_def.items())) #возращает словарь

# def show_post(request, post_slug):
#     post = get_object_or_404(Tupe, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'tupe/post.html', context=context)


class TupeCategory(DataMixin, ListView):
    # paginate_by = 3 #показывает пагинацию cтраниц
    model = Tupe  #подкл к модели
    template_name = 'tupe/index.html' #ссылка на шаблон
    context_object_name = 'posts'  #подл к шаблону индекс
    allow_empty = False #ошибка 404


    #метод который показывает те катег которые выбранные категории
    def get_queryset(self):
        return Tupe.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)#маршутизация по слагу
        #через kwargs получаем все парамет маршрута


    # функция формирует динамич контекст
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))



# def show_category(request, cat_id):
#     posts = Tupe.objects.filter(cat_id=cat_id)
#     params = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'По рубрикам',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'tupe/index.html', params)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm   #название из form.py   #UserCreationForm = форма для регист пользователей
    template_name = 'tupe/register.html'    #ссылка на шаблон
    success_url = reverse_lazy('login') #перенаправление при успешной регист на логин

    # функция формирует динамич контекст
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    #метод вызывается при успешной решистрации
    def form_valid(self, form):
        user = form.save()  #сохраняет в бд пользователя
        login(self.request, user)   #авторизовывает пользователя
        return redirect('home') #переотправляет на главную стр


#LoginView - вся логика авторизации
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm #название в forms.py #AuthenticationForm - стандартная форма авториз
    template_name = 'tupe/login.html'


    #формирование контекста для логина
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


    #вызывается когда пользователь ввел верно логин пароль
    def get_success_url(self):
        return reverse_lazy('home')


#функция выйти
def logout_user(request):
    logout(request)
    return redirect('login')    #переотправляет на login если выйти