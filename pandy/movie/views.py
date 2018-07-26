from django.shortcuts import render
from .models import Movie
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
def index(request):
    movie_list = Movie.objects.order_by('-v_pub_date')[:10]
    context = {
            'movie_list': movie_list,
            }
    return render(request, 'movie/index.html', context)

def movie_search(request, movie_name):
    movie_list = Movie.objects.filter(v_name__icontains=movie_name)[:100]
    context = {
            'movie_list': movie_list,
            }
    return render(request, 'movie/index.html', context)
    # return HttpResponse('search page %s' % movie_name)
    

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id  = movie_id)
    return render(request, 'movie/detail.html', {'movie': movie})
