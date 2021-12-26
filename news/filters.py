from .models import Post
from django_filters import FilterSet, DateFilter
from django.forms import DateInput


class PostFilter(FilterSet):
    # time_in = DateFilter(
    #     lookup_expr='icontains',
    #     widget=DateInput(
    #         attrs={
    #             'type': 'date'
    #         }
    #     )
    # )

    class Meta:
        model = Post
        fields = {'date_time': ['gt'],
                  'title': ['icontains'],
                  'author': ['exact'],
        }
