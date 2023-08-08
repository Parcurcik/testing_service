from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('tests/', views.tests, name='tests'),
    path('test/<int:test_id>/', views.test, name='test'),
    path('test/<int:test_id>/delete_user_answers/', views.delete_user_answers, name='delete_user_answers'),
]
