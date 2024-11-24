from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

app_name = 'core'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='core:home'), name='logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('create-list/', CreateListView.as_view(), name='create_list'),
    path('update-list/<int:list_id>', UpdateListView.as_view(), name='update_list'),
    path('lists/<int:pk>/', ListDetailView.as_view(), name='list_detail'),
]