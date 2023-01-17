from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.conf import settings

from .forms import PostForm
from .models import Group, Post

User = get_user_model()


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(post_list, settings.POSTS_ON_SCREEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'paginator': paginator
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    paginator = Paginator(group.posts.all(), settings.POSTS_ON_SCREEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts = group.posts.all()
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
        'paginator': paginator
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    posts = Post.objects.filter(author=author)
    paginator = Paginator(posts, settings.POSTS_ON_SCREEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = posts.count
    context = {
        'author': author,
        'page_obj': page_obj,
        'post_count': post_count

    }
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_count = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'post_count': post_count
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html',
                               {'form': form}
                      )
    form.instance.author = request.user
    form.save()
    return redirect('post:profile', request.user)


@login_required
def post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form = form.save(False)
        form.author = request.user
        form.save()
        return redirect('post:post_detail', post_id=post.id)
    return render(
        request,
        'posts/create_post.html',
        {'form': form, 'post': post}
    )
