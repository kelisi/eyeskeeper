from django.db import models


# Create your models here.
class Topic(models.Model):
    """测试==用户学习的主题"""
    # CharField：由字符或文本组成的数据
    text = models.CharField(max_length=200)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """"返回模型的字符串表示"""
        return self.text
