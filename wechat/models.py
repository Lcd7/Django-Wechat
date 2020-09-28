from __future__ import unicode_literals

from django.db import models

# Create your models here.
class PersonalLog(models.Model):
    userid = models.CharField('用户id', max_length = 255)
    content = models.TextField(
        '内容', null = True, blank = True, help_text = '记录的内容'
    )
    pub_date = models.DateTimeField('记录时间', auto_now_add = True)

    def __str__(self):
        return self.userid 

class PersonalImg(models.Model):
    userid = models.CharField('用户id', max_length = 255)
    MediaId = models.TextField('通过素材管理中的接口上传多媒体文件，得到的id。')
    PicUrl = models.TextField('图片链接（由系统生成）')
    adminSet = models.BooleanField(default = False)

    def __str__(self):
        return self.MediaId