from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'blogs'

urlpatterns = [
    path('list/', views.blog_list, name='blog_list'),
    path('detail/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('rate/<int:pk>/', views.rate_blog, name='rate_blog'),
    path('create/', views.create_blog, name='create_blog'),
    path('blog/<int:pk>/delete/', views.delete_blog, name='delete_blog'),
    path('search/', views.blog_list, name='blog_search'),
    path('blog_search/', views.blog_search, name='blog_search'),
    path('', views.home_view, name='home'),
    path('about-me/', views.about_me, name='about_me'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)