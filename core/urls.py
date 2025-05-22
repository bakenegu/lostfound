from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('lost/', views.report_lost, name='report_lost'),
    path('found/', views.report_found, name='report_found'),
    path('items/', views.item_list, name='item_list'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
