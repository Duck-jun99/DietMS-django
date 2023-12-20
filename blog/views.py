from django.shortcuts import render
from django.utils import timezone
from blog.forms import PostForm
from .models import Post
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .serializers import PostSerializer
from django.http import JsonResponse

# Create your views here.

def post_list(request):
    posts = Post.objects.all().order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_today(request):
    today = timezone.now().date()
    posts_today = Post.objects.filter(published_date__date=today).order_by('published_date')
    
    return render(request, 'blog/post_list.html', {'posts': posts_today})

def post_not_today(request):
    today = timezone.now().date()
    posts_not_today = Post.objects.exclude(published_date__date=today).order_by('published_date')
    
    return render(request, 'blog/post_list.html', {'posts': posts_not_today})
    

def post_today_app(request):
    today = timezone.now().date()
    posts_today = Post.objects.filter(published_date__date=today).order_by('published_date')
    data = []
    for post in posts_today:
        post_data = {
            'title': post.title,
            'text': post.text,
            'created_date': post.created_date,
            'image': post.image.url if post.image else None,  # 이미지 URL 사용 (이미지가 없을 경우 None)
            'meal': post.meal,
        }
        data.append(post_data)

    return JsonResponse(data, safe=False)
    
def post_not_today_app(request):
    today = timezone.now().date()
    posts_not_today = Post.objects.exclude(published_date__date=today).order_by('published_date')
    data = []
    for post in posts_not_today:
        post_data = {
            'title': post.title,
            'text': post.text,
            'created_date': post.created_date,
            'image': post.image.url if post.image else None,  # 이미지 URL 사용 (이미지가 없을 경우 None)
            'meal': post.meal,
        }
        data.append(post_data)

    return JsonResponse(data, safe=False)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

class IntroducerImage(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer