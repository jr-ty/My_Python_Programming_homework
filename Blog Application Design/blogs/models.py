from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    text = models.TextField(verbose_name="内容")
    date_added = models.DateTimeField(auto_now_add=True)
    # 关联到 User 模型，删除用户时级联删除其文章
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title