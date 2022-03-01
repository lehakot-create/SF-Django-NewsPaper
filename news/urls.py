from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('', cache_page(60)(NewsList.as_view()), name='news_list'),
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('search/', Search.as_view(), name='search'),
    path('search/<int:pk>/', NewsDetailView.as_view()),
    path('category/<int:pk>/', CategoryList.as_view(), name='category_list'),
    # path('category/<int:pk>/', cache_page(300)(CategoryList.as_view()), name='category_list'),
    path('add/', PostCreateView.as_view(), name='add_post'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='update_post'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('upgrade/', upgrade, name='upgrade'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
]
