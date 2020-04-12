from django.shortcuts import render, get_object_or_404
from .models import Article

def all_blogs (request):
    # ORDER BY DATE, LAST 2 ARTICLES
    # LEARN HOW TO PAGINATE VIA LINKS
    articles = Article.objects.order_by('-date')[:2]

    # FETCH ALL ARTICLES
    # articles = Article.objects.all()

    return render(request, 'blog/all_blogs.html', { 'articles': articles })

def detail (request, blog_id):
    # GET ARTICLE OR RETURN 404, "pk" IS PRIMARY KEY
    article = get_object_or_404(Article, pk=blog_id)

    return render(request, 'blog/detail.html', { 'article': article })