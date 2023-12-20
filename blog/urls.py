from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Post', views.IntroducerImage)

urlpatterns = [
    path(r'', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('api_root/', include(router.urls)),
    path('post_today/',views.post_today, name='post_today'),
    path('post_not_today/',views.post_not_today, name='post_not_today'),
    path('post_today_app/',views.post_today_app, name='post_today'),
    path('post_not_today_app/',views.post_not_today_app, name='post_not_today'),

]