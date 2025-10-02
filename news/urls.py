from django.urls import path
from . import views
from .views import (
    NewsCreate, NewsUpdate, NewsDelete,
    ArticleCreate, ArticleUpdate, ArticleDelete
)
from .views import become_author
from .views import subscribe_to_category, unsubscribe_from_category

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('search/', views.news_search, name='news_search'),
    path('become-author/', become_author, name='become_author'),


    # URL для новостей
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    # URL для статей
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

    # URL для подписки/отписки
    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_category'),
    path('category/<int:category_id>/unsubscribe/', unsubscribe_from_category, name='unsubscribe_category'),

    path('my-subscriptions/', views.my_subscriptions, name='my_subscriptions'),

    path('activation-success/', views.activation_success, name='activation_success'),
]




