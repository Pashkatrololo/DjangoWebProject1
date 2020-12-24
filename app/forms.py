"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog
from django.contrib import admin
from .models import Category, Product

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {"text": "Комментарий"}


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image')
        labels = {'title': 'Заголовок', 'description': 'Краткое содержание', 'content': 'Полное содержание', 'image': "Картинка"}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)


class AnketaForm(forms.Form):                                #Анкета
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    city = forms.CharField(label='Ваш город', min_length=2, max_length=100)
    gender = forms.ChoiceField(label='Оцените наш сайт', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')], initial=1)
    internet = forms.ChoiceField(label='С какой проблемой вы столкнулись?',
                                 choices=(('1','Не проходит оплата'),
                                          ('2','Не могу найти нужный товар'),
                                          ('3','Не интуитивный дизайн'),
                                          ('4','Прочее')), initial=1)
    notice = forms.BooleanField(label='Получить ответ на email?', required=False)
    email = forms.EmailField(label='Ваш e-mail', min_length=7)
    message = forms.CharField(label='Коротко о себе', widget=forms.Textarea(attrs={'rows':12, 'cols':20}))