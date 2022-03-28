from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Post, Comment, Author, Category, PostCategory, CategorySubscribers


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostsAdmin(TranslationAdmin):
    model = Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'choices', 'title', 'url')
    search_fields = ('title', 'text')
    ordering = ['-date_time']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'post')


class CategorySubscriberAdmin(admin.ModelAdmin):
    list_display = ('subscribers', 'category')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(CategorySubscribers, CategorySubscriberAdmin)
