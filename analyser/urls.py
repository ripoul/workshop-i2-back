
from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='index'),
    path('api/search', views.search, name='search'),
    path('api/get_all', views.get_all, name='get_all'),
]