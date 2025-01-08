from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from .serializers import UserSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from .models import User
from rest_framework.permissions import IsAuthenticated

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

