from django.urls import path 
from . import views
from django.conf.urls.static import static 
from django.conf import settings
from .views import LikePost, PostDetailView, PostView,PostEditView,PostDeleteView,CommentDelete, ProfileEditView,ProfileView,DislikePost
urlpatterns=[
    path('',views.index,name='base'),
    # path('signup',views.signup,name='signup'),
    # path('login',views.login,name='login'),
    # path('logout',views.logout,name='logout'),
    # path('settings',views.settings,name='settings'),
    path('posts',PostView.as_view(), name='posts') ,
    path('post_single/<int:pk>',PostDetailView.as_view(),name='post_single'),
    path('post_edit/<int:pk>',PostEditView.as_view(),name='post_edit'),
    path('post_delete/<int:pk>',PostDeleteView.as_view(),name='post_delete'),
    path('post_single/<int:post_pk>/comment/delete/<int:pk>/',CommentDelete.as_view(),name='delete_comment'),
    path('profile/<int:pk>',ProfileView.as_view(),name='profile'),
    path('profile_edit/<int:pk>',ProfileEditView.as_view(),name='profile_edit'),
    path('post_single/<int:pk>/like',LikePost.as_view(),name='like_post'),
    path('post_single/<int:pk>/dislike',DislikePost.as_view(),name='dislike_post'),
      
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)