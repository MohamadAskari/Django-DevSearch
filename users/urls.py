from django.urls import path
from . import views

urlpatterns = [
    path('', views.users, name='profiles'),
    path('single-user/<str:pk>', views.singleProfile, name='single profile'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('account/', views.userAccount, name='account'),
    path('edit-profile/', views.editProfile, name='edit profile'),
    path('create-skill/', views.createSkill, name='create skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.viewMessage, name='message'),
    path('send-message/<str:pk>/', views.sendMessage, name='send message'),
]