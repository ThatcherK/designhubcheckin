from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('login/', views.login, name="login"),
    path ('addvisitor/', views.add_new_visitor, name="addvisitor"),
    path('<int:visitor_id>/editvisitor/', views.check_in_returning_visitor, name='edit')
     
]