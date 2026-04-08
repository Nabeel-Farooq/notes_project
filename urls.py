from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_note, name='create'),
    path('edit/<int:pk>/', views.edit_note, name='edit'),
    path('delete/<int:pk>/', views.delete_note, name='delete'),
    path('share/<uuid:share_id>/', views.view_shared_note, name='share'),
    path('versions/<int:pk>/', views.view_versions, name='versions'),
]