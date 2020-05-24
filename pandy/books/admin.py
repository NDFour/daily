from django.contrib import admin
from .models import Books
'''
from .models import Book_notify
'''

class BooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_title', 'book_author', 'book_category', 'book_rating', 'book_pub_date')

    # 后台点击后修改信息页展示的字段
    '''
    fieldsets = [
            ('基本信息', { 'fields' : ['v_name', 'v_pic', 'v_text_info', 'v_bdpan', 'v_pass', 'v_valid', 'v_href', 'v_belong_to', 'v_views' ]}),
            ('磁力链接', { 'fields' : ['v_ed2k_name', 'v_ed2k', 'v_magnet_name', 'v_magnet']}),
            ('时间戳', {'fields' : ['v_pub_date']}),
            ]
    '''

    # 搜索功能
    search_fields = ('id', 'book_title', 'book_author',)


'''
class Book_notify_Admin(admin.ModelAdmin):
    list_display = ('noty_title', 'noty_author', 'noty_date')

    search_fields = ('noty_title', 'noty_author', 'noty_content')
'''


# Register your models here.
admin.site.register(Books, BooksAdmin)

'''
admin.site.register(Book_notify, Book_notify_Admin)
'''

