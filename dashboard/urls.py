from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^$', views.index, name='list'),
	url(r'^guide$', views.guide, name='guide'),
	url(r'^charts$', views.charts, name='charts'),
	url(r'^tables$', views.tables, name='tables'),
	url(r'^all_poem$', views.all_poem, name='all_poem'),
	url(r'^all_story$', views.all_story, name='all_story'),
	url(r'^all_riddle$', views.all_riddle, name='all_riddle'),
	url(r'^new_poem$', views.new_poem, name='new_poem'),
	url(r'^new_story$', views.new_story, name='new_story'),
	url(r'^new_riddle$', views.new_riddle, name='new_riddle'),
	url(r'^master$', views.master, name='master'),
	
	url(r'api/chart/data/$', views.ChartData.as_view(), name="api-data"),
]
