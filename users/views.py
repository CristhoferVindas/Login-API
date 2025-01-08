from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from .serializers import UserSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError

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
