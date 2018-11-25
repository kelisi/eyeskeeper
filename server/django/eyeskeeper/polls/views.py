from django.db.models import F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST 是一个类字典对象，可以通过关键字的名字获取提交的数据，value永远是字符串
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': '请选择一个选项！',
        })
    else:
        # 对指定的选择 得票数 加一
        # 使用F() 避免并发修改的问题
        # https://docs.djangoproject.com/zh-hans/2.1/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # HttpResponseRedirect：参数：用户将要被重定向的URL
        # reverse()：避免了我们在视图函数中硬编码URL，它需要我们给出我们想要跳转的视图的名字和该视图所对应的 URL 模式中需要给该视图提供的参数。
        # 在此reverse() 调用将返回一个这样的字符串：'/polls/<question_id>/results/'
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("你正在对问题 %s 投票。" % question_id)


'''
#基础实现方式
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list':
            latest_question_list,
    }

    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # 方式1
    """
    try:
        question = Question.objects.get(pk=question_id)

    except Question.DoesNotExist:
        raise Http404("问题不存在")
    """
    # 方式2 便捷get
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/results.html', {'question': question})
    # return HttpResponse("你正在查找问题 %s 的结果。" % question_id)

'''
