from django.contrib import admin
from .models import Article

# Register your models here.
class Article_Admin(admin.ModelAdmin):
    list_display = ('title', 'author', 'article_type', 'prior', 'display', 'article_views', 'article_pub_date')
    search_fields = ('title', 'author', 'body')


admin.site.register(Article, Article_Admin)
