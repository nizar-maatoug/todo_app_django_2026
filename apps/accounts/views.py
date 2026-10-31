
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer
)


class RegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED
        )


class LoginView(TokenObtainPairView):

    permission_classes = [AllowAny]

    serializer_class = CustomTokenObtainPairSerializer


class RefreshView(TokenRefreshView):

    permission_classes = [AllowAny]


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)

            # Ensure users can only revoke their own token.
            if str(token["user_id"]) != str(request.user.pk):
                return Response(
                    {"detail": "Invalid refresh token."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token.blacklist()

            return Response(
                status=status.HTTP_205_RESET_CONTENT
            )

        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)
