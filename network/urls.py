from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following, name="following"),
    path("<str:username>", views.profile, name="profile"),
    path('createpost/', views.create_post, name='createpost'),
    path("post/<int:post_id>/comments", views.comment, name="comments"),
    path("post/<int:post_id>/write_comment", views.comment, name="writecomment"),
    path("post/<int:post_id>/delete", views.delete_post, name="deletepost"),
    path("<str:username>/follow", views.follow, name="followuser"),
    path('profile/edit/<str:username>/', views.edit_profile, name='editprofile'), 
    path('toggle_like/<int:id>/', views.toggle_like, name='toggle_like'),
    path('user_activity_chart/', views.user_activity_chart, name='user_activity_chart'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
