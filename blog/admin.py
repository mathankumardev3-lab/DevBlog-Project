from django.contrib import admin
from .models import Post,Category,Tag,Comment,Like,Bookmark
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=("title","author","status","category","views","created_at")
    list_filter=("status","category","created_at")
    search_fields=("title","content","excerpt")
    prepopulated_fields={"slug":("title",)}
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Bookmark)
