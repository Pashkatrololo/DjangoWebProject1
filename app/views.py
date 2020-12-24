"""
Definition of views.
"""

from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm
from django.shortcuts import get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .forms import AnketaForm


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Наша контактная страница',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О сайте',
            'message':'Здесь вы можете узнать о нас!',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Здесь вы можете узнать о смежных сайтах, которые помогут вам определиться с выбором оборудования',
            'year':datetime.now().year,
        }
    )



def registration(request):

    """Renders the registration page."""

    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки формы

        regform = UserCreationForm (request.POST)

        if regform.is_valid(): #валидация полей формы

            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы

            reg_f.is_staff = False # запрещен вход в административный раздел

            reg_f.is_active = True # активный пользователь

            reg_f.is_superuser = False # не является суперпользователем

            reg_f.date_joined = datetime.now() # дата регистрации

            reg_f.last_login = datetime.now() # дата последней авторизации

            reg_f.save() # сохраняем изменения после добавления данных

            return redirect('home') # переадресация на главную страницу после регистрации

    else:

        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    return render(

        request,

        'app/registration.html',

        {

            'regform': regform, # передача формы в шаблон веб-страницы

            'year':datetime.now().year,

        }

    )

def blog(request):

    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year' : datetime.now().year
        }
    )

def blogpost(request, parametr):

    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()

            return redirect("blogpost", parametr=post_1.id)
    else:
        form = CommentForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year':datetime.now().year,
        }
     )

def newpost(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()
    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Видеофайлы!',
            'year':datetime.now().year,
        }
    )

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'app/product_list.html', #Путь до файла с каталогом
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'app/detail.html', {'product': product, #Поменять путь, если не сработает
                                                        'cart_product_form': cart_product_form})

def feedback(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5'}
    internet = {'1': 'Не проходит оплата', '2': 'Не могу найти нужный товар', '3': 'Не интуитивный дизайн', '4': 'Прочее'}
    if request.method == 'POST':
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['internet'] = internet[ form.cleaned_data['internet'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form= None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/pool.html',
        {
            'form':form,
            'data':data
         }
    )