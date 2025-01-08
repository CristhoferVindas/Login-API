from django.urls import path
from .views import CreateUserView,TokenView, LogoutView,UserProfileView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('token/', TokenView.as_view(), name='token'),
    path('logout/', LogoutView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='register'),
    path('refresh/', RefreshTokenView.as_view(), name='register'),
]
