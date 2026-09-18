from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name=models.CharField(max_length=100, unique=True)
    slug=models.SlugField(unique=True, blank=True)
    def save(self,*args,**kwargs):
        if not self.slug: self.slug=slugify(self.name)
        super().save(*args,**kwargs)
    def __str__(self): return self.name

class Tag(models.Model):
    name=models.CharField(max_length=50, unique=True)
    slug=models.SlugField(unique=True, blank=True)
    def save(self,*args,**kwargs):
        if not self.slug: self.slug=slugify(self.name)
        super().save(*args,**kwargs)
    def __str__(self): return self.name

class Post(models.Model):
    STATUS_CHOICES=[("draft","Draft"),("published","Published")]
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True, blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name="posts")
    tags=models.ManyToManyField(Tag,blank=True,related_name="posts")
    content=models.TextField()
    excerpt=models.CharField(max_length=300,blank=True)
    featured_image=models.ImageField(upload_to="posts/",blank=True,null=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="draft")
    views=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["-created_at"]
    def save(self,*args,**kwargs):
        if not self.slug: self.slug=slugify(self.title)
        super().save(*args,**kwargs)
    def get_absolute_url(self): return reverse("post_detail",kwargs={"slug":self.slug})
    def __str__(self): return self.title

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created_at"]

class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta: constraints=[models.UniqueConstraint(fields=["post","user"],name="unique_post_like")]

class Bookmark(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="bookmarks")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta: constraints=[models.UniqueConstraint(fields=["post","user"],name="unique_post_bookmark")]
