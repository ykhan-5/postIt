from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
     path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('login/', views.login_user,name='login'),
    path('logout', views.logout_user,name='logout'),
    path('register/', views.register_user,name='register'),
    path('update_user/', views.update_user,name='update_user'),
    path('peep_like/<int:pk>', views.peep_like, name='peep_like'),
    path('peep_show/<int:pk>', views.peep_show, name='peep_show'),
    path('delete_peep/<int:pk>', views.delete_peep, name='delete_peep'),
    path('edit_peep/<int:pk>', views.edit_peep, name='edit_peep'),
    path('search/', views.search,name='search'),
]
