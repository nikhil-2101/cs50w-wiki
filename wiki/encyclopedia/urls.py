from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<str:entry>/', views.wiki, name='wiki'),
    path('search/', views.search, name='search'),
    path('create/', views.entry_form, name='new_entry'),
    path('random/', views.random_entry, name='random_entry'),
    path('edit/<str:entry>/', views.entry_form, name='edit_entry'),
]