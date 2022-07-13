from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from blog.forms import AddPostForm, RegisterUserForm, LoginUserForm
from blog.models import *
from blog.utils import DataMixin

menu=[{'title':"О сайте", 'url_name':'about'},
      {'title':"Добавить новость", 'url_name':'add_page'},
      {'title':"Обратная связь", 'url_name':'contact'},
      #{'title':"Войти", 'url_name':'login'},
]

class RegisterUser(DataMixin,CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Регистрация")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user=form.save()
        login(self.request,user)
        return redirect('home')


class LoginUser(DataMixin,LoginView):
    form_class=LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self, *,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        c_def=self.get_user_context(title="Авторизация")
        return dict(list(context.items())+list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')

# def addpage(request):
#     if request.method=='POST':
#         form = AddPostForm(request.POST,request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("home")
#     else:
#         form = AddPostForm()
#     #form['is_published'].initial=True
#     return render(request, 'blog/addpage.html',{'form':form,'menu':menu,'title':"Добавить пост"})
#
#
def contact(request):
    return render(request, 'blog/contacts.html', {'menu':menu,'title': 'Обратная связь'})

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Добавление новости'
        context['menu']=menu
        return context

# class PostCategory(ListView):
#     model=Post
#     template_name = 'blog/index.html'
#     context_object_name = 'posts'
#     allow_empty = False
#
#     def get_queryset(self):
#         return Post.objects.filter(cat__slug=self.kwargs['cat_slug'],is_published=True)
#
#     def get_context_data(self, *,object_list=None,**kwargs):
#         context=super().get_context_data(**kwargs)
#         context['menu']=menu
#         context['title']='Категория-'+str(context['posts'][0].cat)
#         context['cat_selected']=context['posts'][0].cat_id
#         return context
def show_category(request,cat_id):
    posts = Post.objects.filter(cat_id=cat_id,is_published=True)
    cats = Category.objects.all()

    if len(posts)==0:
        raise Http404()

    context = {
        'posts': posts,
        'cats': cats,
        'menu': menu,
        'title': 'Новостные тематики',
        'cat_selected': cat_id,
    }
    return render(request,'blog/index.html', context=context)


class ShowPost(DataMixin,DetailView):
    model=Post
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']=context['post']
        context['menu']=menu
        return context
# def show_post(request,post_slug):
#     post = get_object_or_404(Post, pk=post_slug)
#
#     context = {
#         'posts': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#     return render(request, 'blog/post.html', context=context)



#def login(request):
    #return HttpResponse('Авторизация')

class BlogHome(ListView):
    model=Post
    template_name='blog/index.html'
    context_object_name = 'posts'
    extra_context = {'title':"Главная страница"}


    def get_context_data(self, *,object_list=None,**kwargs):
        context=super().get_context_data(**kwargs)
        context['menu']=menu
        context['title']='Главная страница'
        context['cat_selected']=0
        return context

    def get_queryset(self):

        return Post.objects.filter(is_published=True)[:5]

# def index(request):
#     posts=Post.objects.all()
#     cats=Category.objects.all()
#     #if len(posts)==0:
#         #raise Http404()
#
#     context={
#         'posts': posts,
#         'cats':cats,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected':0,
#     }
#     return render(request,'blog/index.html', context=context) #index

def about(request):
    return render(request, 'blog/about.html', {'menu':menu,'title': 'О сайте'}) #about


def topics(request, cat):
    print(request.GET)
    return HttpResponse(f"<h1>Новости по блогам</h1><p>{cat}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
