from django.urls import path
from .views import *
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/signup/', signup, name='signup'),
    path('home/login/', login, name='login'),
    path('home/logout/', logout, name='logout'),
    path('home/', home, name='home'),
    path('home/app_login', views.app_login, name='app_login'),
    path('home/user_json', views.user_json, name='user_json'),
    path('home/update/', update, name='update'),
    path('home/app_signup', views.app_signup, name='app_signup'),
    path('home/app_update', views.app_update, name='app_update'),
] 
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

