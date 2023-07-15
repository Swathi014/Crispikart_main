from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('/add', views.add, name='add'),
    path('/edit', views.edit, name='edit'),
    path('/update', views.update, name='update'),
    path('/delete', views.delete, name='delete')
]
