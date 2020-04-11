from django.shortcuts import render
from .models import Article

def all_blogs (request):
    # ORDER BY DATE, LAST 2 ARTICLES
    # LEARN HOW TO PAGINATE VIA LINKS
    articles = Article.objects.order_by('-date')[:2]

    # FETCH ALL ARTICLES
    # articles = Article.objects.all()

    return render(request, 'blog/all_blogs.html', { 'articles': articles })