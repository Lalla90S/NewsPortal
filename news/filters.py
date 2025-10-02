import django_filters
from django import forms
from .models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название содержит',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    author__user__username = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора содержит',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    created_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label='Опубликовано после',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = []


