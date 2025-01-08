from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from .serializers import UserSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from .models import User
from rest_framework.permissions import IsAuthenticated
from tokenize import TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from django.http import JsonResponse

class CreateUserView(APIView):
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            try:
                validate_password(password)
            except ValidationError as e:
                return Response({"error": e.messages}, status=400)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User created successfully!",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=201)
        return Response(serializer.errors, status=400)

class TokenView(APIView):
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=400)
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            else:
                return Response({"error": "Invalid credentials"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=200)

        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=400)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=400)

        try:
            validate_password(new_password)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully"}, status=200)
        except ValidationError as e:
            return Response({"error": e.messages}, status=400)

class RefreshTokenView(TokenRefreshView):
    throttle_classes = [UserRateThrottle]


def custom_error_404(request, exception):
    return JsonResponse({"error": "The endpoint was not found"}, status=404)

def custom_error_500(request):
    return JsonResponse({"error": "Internal server error"}, status=500)
