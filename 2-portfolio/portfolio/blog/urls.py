from django.urls import path
from . import views

# "app_name" FORCES LINKS TO SPECIFY A NAMESPACE
# INSTEAD OF GENERAL {% url 'detail' %}
# BECOMES APP-SPECIFIC {% url 'blog:detail' %} AND {% url 'blog:all_blogs' %}
app_name = 'blog'

urlpatterns = [
    # /blog/
    path('', views.all_blogs, name='all_blogs'),
    path('<int:blog_id>/', views.detail, name='detail'),
]