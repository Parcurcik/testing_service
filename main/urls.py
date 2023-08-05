from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('tests/', views.tests, name='tests'),
    path('add_test/', views.add_test, name='add_test'),
    path('test/<int:test_id>/', views.test, name='test'),
]
