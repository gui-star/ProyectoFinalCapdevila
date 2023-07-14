from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from django.core.paginator import Paginator


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('blogs:blog_detail', pk=blog.pk)
    else:
        form = CommentForm()

    rating_form = RatingForm()

    # Verificar si el usuario ya ha valorado este blog
    has_rated_blog = Rating.objects.filter(blog=blog, user=request.user).exists()

    # Obtener la calificación actual del usuario para este blog
    user_rating = None
    if has_rated_blog:
        user_rating = Rating.objects.get(blog=blog, user=request.user).rating

    context = {
        'blog': blog,
        'comments': comments,
        'form': form,
        'rating_form': rating_form,
        'has_rated_blog': has_rated_blog,
        'user_rating': user_rating
    }

    return render(request, 'blog_detail.html', context)


@login_required
def rate_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = request.user

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating_value = rating_form.cleaned_data['rating']

            # Verificar si el usuario ya ha valorado este blog
            existing_rating = Rating.objects.filter(blog=blog, user=user).first()
            if existing_rating:
                existing_rating.rating = rating_value
                existing_rating.save()
            else:
                rating = Rating(blog=blog, user=user, rating=rating_value)
                rating.save()

            # Recalcular el rating promedio del blog
            blog.calculate_average_rating()

            messages.success(request, '¡Calificación enviada con éxito!')
            return redirect('blogs:blog_detail', pk=blog.pk)
        else:
            messages.error(request, 'Error en el formulario de calificación')
    else:
        rating_form = RatingForm()

    # Verificar si el usuario ya ha valorado este blog
    has_rated_blog = Rating.objects.filter(blog=blog, user=user).exists()

    # Obtener la calificación actual del usuario para este blog
    user_rating = None
    if has_rated_blog:
        user_rating = Rating.objects.get(blog=blog, user=user).rating

    context = {
        'blog': blog,
        'rating_form': rating_form,
        'has_rated_blog': has_rated_blog,
        'user_rating': user_rating
    }

    return render(request, 'blog_detail.html', context)



@login_required
def create_blog(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blogs:blog_detail', pk=blog.pk)
    else:
        form = CreateBlogForm()
    return render(request, 'create_blog.html', {'form': form})


@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    # Verificar si el usuario actual es el autor original del blog
    if blog.author != request.user:
        messages.error(request, 'No tienes permiso para eliminar este blog')
        return redirect('blogs:blog_detail', pk=blog.pk)

    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog eliminado con éxito')
        return redirect('blogs:blog_list')

    return render(request, 'delete_blog.html', {'blog': blog})


def blog_list(request):
    blogs = Blog.objects.order_by('-date')  # Ordenar por fecha de manera descendente
    paginator = Paginator(blogs, 4)  # Mostrar 4 blogs por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog_list.html', {'page_obj': page_obj})


def home_view(request):
    latest_blogs = Blog.objects.order_by('-date')[:2]
    context = {
        'latest_blogs': latest_blogs
    }
    return render(request, 'home.html', context)

def about_me(request):
    return render(request, 'about_me.html')

def blog_search(request):
    query = request.GET.get('q')
    blogs = Blog.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by('-date')

    paginator = Paginator(blogs, 4)  # Mostrar 4 blogs por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj
    }
    return render(request, 'blog_search.html', context)