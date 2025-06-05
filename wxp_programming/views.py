from django.shortcuts import render
from posts.models import Post
from categories.models import Category
from django.db.models import Q

def home(request, category_slug = None):
    data = Post.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Post.objects.filter(category = category)
    categories = Category.objects.all()
    for cat in categories:
        print(cat.slug, '@@2')
    return render(request, 'home.html', {'data': data, 'category': categories})

def search_posts(request):
    qurey = request.GET.get('q')
    if qurey:
        title_query = Q(title__icontains=qurey)
        content_query = Q(content__icontains=qurey)
        categories_query = Q(category__name__icontains = qurey)

        search = Post.objects.filter(title_query | content_query | categories_query).distinct()
    else:
        search = Post.objects.all()
    categories = Category.objects.all()
    return render(request, './home.html', {'data' : search, 'categories' : categories})