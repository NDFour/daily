from django.contrib import admin
from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ('v_name', 'v_pub_date')

    # 搜索功能
    search_fields = ('v_name',)
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(MovieAdmin, self).get_search_results(request, queryset, search_term)
        try:
            queryset = self.model.objects.filter(v_name__icontains=search_term)
        except:
            pass
        return queryset, use_distinct

# Register your models here.
admin.site.register(Movie, MovieAdmin)
