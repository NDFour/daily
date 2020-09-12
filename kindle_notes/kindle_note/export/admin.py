from django.contrib import admin
from .models import Upload_Record

# Register your models here.
class Upload_RecordAdmin(admin.ModelAdmin):
	list_display = ('id', 'file_name', 'mail_addr', 'message', 'export_info', 'mail_state', 'upload_time')

admin.site.register(Upload_Record, Upload_RecordAdmin)


