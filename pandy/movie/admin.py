from django.contrib import admin
from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'v_name', 'v_valid', 'v_pub_date')

    # 后台点击后修改信息页展示的字段
    fieldsets = [
            ('基本信息', { 'fields' : ['v_name', 'v_pic', 'v_text_info', 'v_bdpan', 'v_pass', 'v_valid', 'v_href' ]}),
            ('磁力链接', { 'fields' : ['v_ed2k_name', 'v_ed2k', 'v_magnet_name', 'v_magnet']}),
            ('时间戳', {'fields' : ['v_pub_date']}),
            ]

    # 搜索功能
    search_fields = ('v_name','id',)
    '''
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(MovieAdmin, self).get_search_results(request, queryset, search_term)
        try:
            queryset = self.model.objects.filter(v_name__icontains=search_term)
        except:
            pass
        return queryset, use_distinct
    '''

# Register your models here.
admin.site.register(Movie, MovieAdmin)
