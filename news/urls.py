from django.urls import path
from .views import NewsList, NewsDetail, CommentDetail

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view())  # , CommentDetail.as_view),
]