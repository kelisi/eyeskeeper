import datetime

from django.db import models

# Create your models here.
from django.db.models import Model
from django.utils import timezone


class AbstractQuestion(Model):
    question_text = models.CharField(max_length=200)

    class Meta:
        abstract = True;


class Question(AbstractQuestion):
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)

    # 方便日志打印相关查看，类似于java toString
    def __str__(self):
        return self.question_text

    class Meta:
        db_table = "t_polls_question"


class Choice(Model):
    # 多对一的关系型数据库，会自动创建数据库索引，db_index = false 可关闭索引
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        db_table = "t_polls_choice"


"""
class AbstractCar(Model):
    manufacturer = models.ForeignKey(
        # 可使用 app_label 寻找所关联的数据表，可使用此方式实现循环关联
        'Manufacturer',
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = True


class Manufacturer(Model):
    pass
"""
