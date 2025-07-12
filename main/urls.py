from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('result/', views.result, name='result'),
    path('add/', views.add_list, name='add'),
    path('edit/<int:list_id>/', views.edit_list, name='edit'),
    path('delete/<int:list_id>/', views.delete_list, name='delete'),
    path('register/', views.register, name='register'),
]

urlpatterns += [
    path('api/lists',views.my_lists, name='my_lists' ),
    path('api/lists/<list_id>',views.get_list, name='get_list' ),
    path('api/lists/<list_id>/result',views.get_result, name='get_result' ),
]