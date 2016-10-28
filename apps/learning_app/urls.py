from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='redirect'),
        url(r'^q_of_day$', views.q_of_day, name='q_of_day'),
        url(r'^q_of_day_answer/(?P<id>\d+)$', views.q_of_day_answer, name='q_of_day_answer'),
        url(r'^correct/(?P<id>\d+)$', views.correct, name='correct'),
        url(r'^correct_page', views.correct_page, name='correct_page'),
        url(r'^progress$', views.progress, name='progress'),
        url(r'^third_answer/(?P<id>\d+)$', views.third_answer, name='third_answer'),
        url(r'^console$', views.console, name='console'),
        url(r'^set_qofd/(?P<id>\d+)$', views.set_qofd, name='set_qofd'),
        url(r'^logout$', views.logout, name='logout'),
        url(r'^student_detail/(?P<id>\d+)$', views.student_detail, name='student_detail'),
        url(r'^stuck$', views.stuck, name='stuck'),
        url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    ]
