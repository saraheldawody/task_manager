from django.urls import path 
from . import views 

urlpatterns = [ 
	path('create/', views.create_task.as_view(), name ='create'), 
    path('tasks/',views.get_all_tasks.as_view(), name='tasks'),
    path('proceed/',views.proceed.as_view(), name='proceed'),
    path('link/',views.link_tasks.as_view(), name='link'),
    path('update/<int:id>',views.update_task.as_view(), name='update'),
    path('find/<int:id>',views.get_task.as_view(), name='find')

] 
