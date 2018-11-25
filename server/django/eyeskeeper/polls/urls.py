from django.urls import path

from . import views

# 修改template中url含此命名空间的url ex：polls:detail
app_name = 'polls'
'''
# 旧的实现方式
urlpatterns = [
    # ex:/polls/
    # the 'name' value as called by the {% url %} template tag
    path('', views.index, name='index'),
    # ex:/polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex:/polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex:/polls/5/vote/
    path('<int:question_id>/vote/', views.votes, name='vote'),
]
'''
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
