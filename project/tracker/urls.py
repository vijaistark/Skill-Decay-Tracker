from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('skills/', views.skills, name='skills'),
    path('skill/add/', views.add_skill, name='add_skill'),
    path('skill/<int:skill_id>/edit/', views.edit_skill, name='edit_skill'),
    path('skill/<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),
    path('skill/<int:skill_id>/log/', views.log_practice, name='log_practice'),
    path('skill/<int:skill_id>/detail/', views.skill_detail, name='skill_detail'),
]
