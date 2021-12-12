from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', news_detail, name='news_detail'),
    path('search/', Search.as_view(), name='search'),
    path('search/<int:pk>/', news_detail),
    path('category/<int:pk>/', CategoryList.as_view(), name='category_list'),
    path('add/', PostCreateView.as_view(), name='add_post'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='update_post'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('upgrade/', upgrade, name='upgrade'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
]
