from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import home, LoginView

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
