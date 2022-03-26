from rest_framework import serializers
from .models import Post


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'choices', 'date_time', 'title', 'text', 'rating', 'url',)
