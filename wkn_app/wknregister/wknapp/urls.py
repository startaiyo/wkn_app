from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name ='index'),
    path('home/', views.home,name="home"),
    path('create/', views.UserCreateView.as_view(),name="create"),
]