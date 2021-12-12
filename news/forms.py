from .models import Post, Comment
from django import forms
from django.forms import CharField, EmailField, IntegerField, ModelForm
from django.contrib.auth.models import Group, User
from allauth.account.forms import SignupForm


class PostForm(ModelForm):
    # author = User.objects.get(id=18)
    # date_time = DateTimeField(widget=DateTimeInput, input_formats='')
    # date_time = datetime.now()
    # print(date_time)

    class Meta:
        model = Post
        fields = [#'author',
                  'choices',
                  'category',
                  'title',
                  'text']


class CommentForm(ModelForm):
    text = CharField(label='Текст комментария:', max_length=256)

    class Meta:
        model = Comment
        fields = ['text']


# class NewCommentForm(ModelForm):
#     text = CharField(label='New comment:',
#                      max_length=128)


class BaseRegisterForm(SignupForm):

    def save(self, request):
        user = super(BaseRegisterForm, self).save(request)
        group = Group.objects.get(name='common')
        group.user_set.add(user)
        return user


class SignupForm(forms.ModelForm):

    def signup(self, request, user):
        group = Group.objects.get(name='common')
        user.groups.add(group)
        user.save()


class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email']

