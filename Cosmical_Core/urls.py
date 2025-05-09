from django.urls import path
from . import views
from .views import CreateThread, ListThreads, ThreadView, CreateMessage

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('like-post', views.like_post, name='like-post'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('search', views.search, name='search'),
    path('delete-post/<uuid:post_id>/', views.delete_post, name='delete-post'),
    path('edit-post/<uuid:post_id>/', views.edit_post, name='edit-post'),
    path('save-post/<uuid:post_id>/', views.save_post, name='save-post'),
    path('report-post/<uuid:post_id>/', views.report_post, name='report-post'),
    path('inbox/', ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),
]