from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post
from .filters import PostFilter
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import PostForm
from .models import Post, Author
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Category
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_page




@cache_page(60 * 5)  # Кэшируем на 5 минут
def news_list(request):
    # Получаем все новости и статьи, отсортированные от новых к старым
    posts_list = Post.objects.all().order_by('-created_at')

    # Добавляем пагинацию - 10 новостей на страницу
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_list.html', {'page_obj': page_obj})


@cache_page(60 * 15)  # Кэшируем на 15 минут (статьи редко меняются)
def news_detail(request, news_id):
    # Получаем конкретную новость/статью по ID или показываем 404
    post = get_object_or_404(Post, id=news_id)
    return render(request, 'news/news_detail.html', {'post': post})


from django.shortcuts import render


@cache_page(60 * 2)  # Кэшируем на 2 минуты (поиск часто меняется)
def news_search(request):
    # Получаем все новости
    posts_list = Post.objects.all().order_by('-created_at')

    # Применяем фильтры
    post_filter = PostFilter(request.GET, queryset=posts_list)

    # Добавляем пагинацию к отфильтрованным результатам
    paginator = Paginator(post_filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_search.html', {
        'filter': post_filter,
        'page_obj': page_obj
    })



# Представления для новостей
class NewsCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    login_url = '/admin/login/'

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.NEWS

        # Назначаем автора - получаем или создаем Author для текущего пользователя
        user = self.request.user
        author, created = Author.objects.get_or_create(user=user)
        post.author = author

        # Сохраняем пост
        response = super().form_valid(form)

        # ОТПРАВЛЯЕМ УВЕДОМЛЕНИЯ ПОДПИСЧИКАМ ЧЕРЕЗ CELERY
        from .tasks import send_new_post_notification
        send_new_post_notification.delay(self.object.id)

        return response

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'news_id': self.object.id})






class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    permission_required = 'news.change_post'  # ← ДОБАВЬТЕ ЭТУ СТРОКУ

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'news_id': self.object.id})



class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')



# Представления для статей
class ArticleCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    login_url = '/admin/login/'

    def get_form_kwargs(self):
        """Передаем текущего пользователя в форму"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = Post.ARTICLE

        # Назначаем автора - получаем или создаем Author для текущего пользователя
        user = self.request.user
        author, created = Author.objects.get_or_create(user=user)
        post.author = author

        # Сохраняем пост
        response = super().form_valid(form)

        # ОТПРАВЛЯЕМ УВЕДОМЛЕНИЯ ПОДПИСЧИКАМ ЧЕРЕЗ CELERY
        from .tasks import send_new_post_notification
        send_new_post_notification.delay(self.object.id)

        return response

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'news_id': self.object.id})


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    permission_required = 'news.change_post'  # ← ДОБАВЬТЕ ЭТУ СТРОКУ

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'news_id': self.object.id})


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib import messages


@login_required
def become_author(request):
    """Добавляет пользователя в группу authors"""
    user = request.user
    authors_group = Group.objects.get(name='authors')

    if not user.groups.filter(name='authors').exists():
        user.groups.add(authors_group)
        messages.success(request, 'Поздравляем! Теперь вы автор и можете создавать и редактировать новости и статьи.')
    else:
        messages.info(request, 'Вы уже являетесь автором.')

    return redirect('news_list')


@login_required
def subscribe_to_category(request, category_id):
    """Подписка пользователя на категорию"""
    category = get_object_or_404(Category, id=category_id)
    user = request.user

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        messages.success(request, f'Вы успешно подписались на категорию "{category.name}"')
    else:
        messages.info(request, f'Вы уже подписаны на категорию "{category.name}"')

    # Возвращаем на предыдущую страницу
    return redirect(request.META.get('HTTP_REFERER', 'news_list'))


@login_required
def unsubscribe_from_category(request, category_id):
    """Отписка пользователя от категории"""
    category = get_object_or_404(Category, id=category_id)
    user = request.user

    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
        messages.success(request, f'Вы отписались от категории "{category.name}"')
    else:
        messages.info(request, f'Вы не подписаны на категорию "{category.name}"')

    # Возвращаем на предыдущую страницу
    return redirect(request.META.get('HTTP_REFERER', 'news_list'))


@login_required
def my_subscriptions(request):
    """Страница управления подписками пользователя"""
    user = request.user
    subscribed_categories = Category.objects.filter(subscribers=user)
    all_categories = Category.objects.all()

    return render(request, 'news/my_subscriptions.html', {
        'subscribed_categories': subscribed_categories,
        'all_categories': all_categories,
    })

def activation_success(request):
    """Страница успешной активации"""
    return render(request, 'news/activation_success.html', {
        'user': request.user
    })
# Create your views here.
@login_required
def subscribe_category(request, category_id):
    """
    Подписка пользователя на категорию
    """
    category = get_object_or_404(Category, id=category_id)

    # Проверяем, не подписан ли уже пользователь
    if not category.subscribers.filter(id=request.user.id).exists():
        category.subscribers.add(request.user)
        messages.success(request, f'✅ Вы успешно подписались на категорию "{category.name}"')
        print(f"✅ Пользователь {request.user.username} подписался на категорию {category.name}")
    else:
        messages.info(request, f'ℹ️ Вы уже подписаны на категорию "{category.name}"')

    # Возвращаем на страницу подписок
    return redirect('my_subscriptions')


@login_required
def unsubscribe_category(request, category_id):
    """
    Отписка пользователя от категории
    """
    category = get_object_or_404(Category, id=category_id)

    # Проверяем, подписан ли пользователь
    if category.subscribers.filter(id=request.user.id).exists():
        category.subscribers.remove(request.user)
        messages.success(request, f'✅ Вы отписались от категории "{category.name}"')
        print(f"❌ Пользователь {request.user.username} отписался от категории {category.name}")
    else:
        messages.info(request, f'ℹ️ Вы не были подписаны на категорию "{category.name}"')

    # Возвращаем на страницу подписок
    return redirect('my_subscriptions')


@login_required
def my_subscriptions(request):
    """
    Страница с подписками пользователя
    """
    # Получаем категории, на которые подписан пользователь
    subscribed_categories = request.user.subscribed_categories.all()
    # Получаем все категории
    all_categories = Category.objects.all()

    return render(request, 'news/my_subscriptions.html', {
        'subscribed_categories': subscribed_categories,
        'all_categories': all_categories,
    })