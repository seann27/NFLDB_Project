from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'team_info/(?P<id>\d+)/$',views.team_info, name='team_info'),
    url(r'js_event/1/',views.event, name='event'),
    url(r'js_event/2/',views.event2, name='event2'),
    url(r'js_event/3/',views.event3, name='event3'),
    url(r'js_event/4/',views.update_players, name='update_players'),
    url(r'js_event/5/(?P<id>\d+)/$',views.show_players, name='show_players')
]