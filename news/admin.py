from django.contrib import admin
from .models import Post, Comment, Author, Category, PostCategory, CategorySubscribers
from .utils import run_parser


# def run_parse(modeladmin, request, qyeryset):
#     run_parser()
#     run_parse.short_description = 'Запустить парсер новостей'


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'choices', 'title', 'url')
    search_fields = ('title', 'text')
    # actions = [run_parse]


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
