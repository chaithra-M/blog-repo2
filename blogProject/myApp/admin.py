from django.contrib import admin
from myApp.models import Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    l=['title','slug','author','body','publish','create','update','status']
    prepopulated_fields={'slug':('title',)}
    list_filter=['status','create','publish','author']
    search_fields=['title','body']
    raw_id_fields=('author',)
    ordering=['status','publish']
admin.site.register(Post,PostAdmin)
class CommentAdmin(admin.ModelAdmin):
    l=['post','email','body','created','updated','active']
    list_filter=['active','created','updated']
    search_fields=['name','email','body']
admin.site.register(Comment,CommentAdmin)
