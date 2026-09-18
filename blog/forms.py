from django import forms
from .models import Post, Comment, Category, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=["title","excerpt","content","featured_image","category","tags","status"]
        widgets={"content":forms.Textarea(attrs={"rows":14,"class":"form-control"}),
                 "excerpt":forms.Textarea(attrs={"rows":3})}

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["body"]
        widgets={"body":forms.Textarea(attrs={"rows":3,"placeholder":"Write a comment..."})}

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=["name"]

class TagForm(forms.ModelForm):
    class Meta:
        model=Tag
        fields=["name"]
