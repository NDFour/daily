from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from .models import Article

from books.models import Books

# 使用 markdown 写文章
import markdown


# Create your views here.

@cache_page(60 * 15)
def index(request):
    article_list = Article.objects.filter( display = True ).order_by('-prior')
    # article_list = Article.objects.filter( display = True ).order_by('-article_modefy_date')

    resou_book_list = Books.objects.order_by('-book_views')[:10]

    context = {
            'article_list': article_list,
            'resou_book_list': resou_book_list,
            'notifications': article_list,
            }

    return render(request, 'article/index.html', context)


@cache_page(60 * 15)
def article_detail(request, article_id):
    article = get_object_or_404(Article, id  = article_id)
    
    article_list = Article.objects.filter( display = True ).order_by('-prior')

    resou_book_list = Books.objects.order_by('-book_views')[:10]

    try:
	    # 阅读量自增 1
	    article.increase_views()

	    # 将 markdown 语法渲染成 html 样式
	    article.body = markdown.markdown(article.body,
	    	extensions = [
	    	# 包含 缩写、表格等常用扩展
	    	'markdown.extensions.extra',
	    	'markdown.extensions.codehilite',
	    	])
    except Exception as e:
    	pass

    context = {
            'article': article,
            'resou_book_list': resou_book_list,
            'notifications': article_list,
            }

    return render(request, 'article/detail.html', context)
