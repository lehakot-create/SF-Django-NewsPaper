from .models import Post
from django_filters import FilterSet, DateFilter, CharFilter
from django.forms import DateInput


class PostFilter(FilterSet):
    date_time = DateFilter(label='Дата больше чем:',
        lookup_expr='gt',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    title = CharFilter(label='Заголовок содержит:',
                       lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['date_time', 'title', 'author']

