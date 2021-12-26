from django.urls import path
from .views import NewsList, NewsDetail, \
    CommentDetail, Search, CategoryList, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', Search.as_view(), name='search'),
    path('search/<int:pk>/', NewsDetail.as_view()),
    path('category/<int:pk>/', CategoryList.as_view(), name='category_list'),
    path('add/', PostCreateView.as_view(), name='add_post'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='update_post'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
]
