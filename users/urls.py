from django.urls import path
from .views import CreateUserView,TokenView 

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('token/', TokenView.as_view(), name='token'),
]
