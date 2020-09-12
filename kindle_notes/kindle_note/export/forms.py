from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

 
class UploadForm(forms.Form):
    # 生词本文件 .db
    my_file = forms.FileField( required = True)
    # 用户接收邮箱
    # mail_addr = forms.EmailField(required = True)
    # 用户备注信息
    # message = forms.CharField(widget=forms.Textarea)


    # 验证 my_file 合法性
    def clean_my_file(self):
        CONTENT_TYPES = ['txt']
        # 2.5MB - 2621440
        # 5MB - 5242880
        # 10MB - 10485760
        # 20MB - 20971520
        # 50MB - 52428800
        # 100MB 104857600
        # 250MB - 214958080
        # 500MB - 429916160
        MAX_UPLOAD_SIZE = 10485760

        content = self.cleaned_data['my_file']

        # print('content_type:')
        # print(content.content_type)

        # content_type = content.content_type.split('/')[0]
        content_type = content.name.split('.')[-1]

        if content_type in CONTENT_TYPES:
            if content.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError(_('请控制文件大小小于 %s. 当前文件大小： %s') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content.size)))
        else:
            raise forms.ValidationError(_('文件格式错误！'))

        return content

