from django.urls import path
from .views import CreateUserView,TokenView, LogoutView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('token/', TokenView.as_view(), name='token'),
    path('logout/', LogoutView.as_view(), name='register'),
]
