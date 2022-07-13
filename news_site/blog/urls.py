

from django.contrib import admin

from django.urls import path

from blog.views import *


urlpatterns = [
    path('', BlogHome.as_view(),name='home' ),
    path('addpage/', AddPage.as_view(),name='add_page' ),
    path('contact/', contact,name='contact' ),
    path('login/', LoginUser.as_view(),name='login'),
    path('logout/', logout_user,name='logout'),
    # path('category/<slug:cat_slug>', PostCategory.as_view(), name='category'),
    path('category/<int:cat_id>', show_category, name='category'),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='post'),
    path('about/', about, name='about'),
    path('topic/<int:cat>', topics),
    path('registr/',RegisterUser.as_view(),name='register'),
]

