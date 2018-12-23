from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
# Create your models here.


class Comments(models.Model):

    # 关联模型
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 用户
    user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING)

    # 评论内容
    text = models.TextField()
    # 评论时间
    created_time = models.DateTimeField(auto_now_add=True)

    # 顶级评论
    root = models.ForeignKey('self', related_name="root_comment",null=True, on_delete=models.DO_NOTHING)

    # 父亲
    parent = models.ForeignKey('self', related_name="parent_comment",null=True, on_delete=models.DO_NOTHING)
    # 回复谁
    reply_to = models.ForeignKey(User, related_name="replies", null=True,on_delete=models.DO_NOTHING)


    is_deleted = models.BooleanField(default=False)
    #
    # def __str__(self):
    #     return self.text[:20]

    def __str__(self):
        return self.text[:30]

    class Meta:
        ordering = ['created_time']
