"""
/				index
/<slug> 		poem/story/riddle/author
/poems			all poems
/riddles		all riddles
/stories		all stories
/dashboard		@login_required user's panel
/

url(r'^/', )
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import (login_view, logout_view, register_view)
from core.views import author_detail, about
urlpatterns = [

	url(r'^', include('core.urls', namespace="writer")),

	url(r'^admin/', admin.site.urls),
	url(r'^dashboard/', include('dashboard.urls', namespace="dashboard")),
	
	url(r'^about/', about, name='about' ),
	
	url(r'login/',login_view, name='login' ),
	url(r'logout/', logout_view, name='logout'),
	url(r'register/', register_view, name='register'),

	url(r'^(?P<user_name>[\w.@+-]+)/$', author_detail, name='author_detail'),

]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
