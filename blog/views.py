from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Category, Tag, Comment, Like, Bookmark
from .forms import PostForm, CommentForm

def home(request):
    posts=Post.objects.filter(status="published").select_related("author","category").prefetch_related("tags")
    q=request.GET.get("q","").strip()
    category=request.GET.get("category","")
    tag=request.GET.get("tag","")
    if q: posts=posts.filter(Q(title__icontains=q)|Q(content__icontains=q)|Q(excerpt__icontains=q))
    if category: posts=posts.filter(category__slug=category)
    if tag: posts=posts.filter(tags__slug=tag)
    paginator=Paginator(posts,6)
    page=paginator.get_page(request.GET.get("page"))
    return render(request,"blog/home.html",{"page":page,"categories":Category.objects.all(),"tags":Tag.objects.all(),"q":q})

def post_detail(request,slug):
    post=get_object_or_404(Post.objects.select_related("author","category"),slug=slug,status="published")
    Post.objects.filter(pk=post.pk).update(views=F("views")+1)
    post.refresh_from_db()
    if request.method=="POST" and request.user.is_authenticated:
        form=CommentForm(request.POST)
        if form.is_valid():
            c=form.save(commit=False); c.post=post; c.author=request.user; c.save()
            messages.success(request,"Comment added.")
            return redirect(post.get_absolute_url())
    else: form=CommentForm()
    related=Post.objects.filter(status="published").exclude(pk=post.pk)
    if post.category: related=related.filter(category=post.category)
    return render(request,"blog/post_detail.html",{"post":post,"comment_form":form,"related":related[:3]})

@login_required
def post_create(request):
    form=PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        post=form.save(commit=False); post.author=request.user; post.save(); form.save_m2m()
        messages.success(request,"Post created.")
        return redirect(post.get_absolute_url() if post.status=="published" else "dashboard")
    return render(request,"blog/post_form.html",{"form":form,"title":"Create Post"})

@login_required
def post_edit(request,slug):
    post=get_object_or_404(Post,slug=slug,author=request.user)
    form=PostForm(request.POST or None,request.FILES or None,instance=post)
    if form.is_valid():
        form.save(); messages.success(request,"Post updated."); return redirect(post.get_absolute_url() if post.status=="published" else "dashboard")
    return render(request,"blog/post_form.html",{"form":form,"title":"Edit Post"})

@login_required
def post_delete(request,slug):
    post=get_object_or_404(Post,slug=slug,author=request.user)
    if request.method=="POST": post.delete(); messages.success(request,"Post deleted."); return redirect("dashboard")
    return render(request,"blog/confirm_delete.html",{"post":post})

@login_required
def dashboard(request):
    posts=Post.objects.filter(author=request.user)
    return render(request,"blog/dashboard.html",{"posts":posts})

@login_required
def toggle_like(request,slug):
    post=get_object_or_404(Post,slug=slug,status="published")
    obj,created=Like.objects.get_or_create(post=post,user=request.user)
    if not created: obj.delete()
    return redirect(post.get_absolute_url())

@login_required
def toggle_bookmark(request,slug):
    post=get_object_or_404(Post,slug=slug,status="published")
    obj,created=Bookmark.objects.get_or_create(post=post,user=request.user)
    if not created: obj.delete()
    messages.success(request,"Bookmark updated.")
    return redirect(post.get_absolute_url())

@login_required
def bookmarks(request):
    posts=Post.objects.filter(bookmarks__user=request.user,status="published")
    return render(request,"blog/bookmarks.html",{"posts":posts})
