from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        from .serializers import UserSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user


class VerifyEmailView(APIView):
    """
    Simple email verification (for demo).
    In real production, you’d use tokens/links.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_verified = True
        user.save()
        return Response({"message": "Email verified successfully!"})

class ActivateAccountView(APIView):
    """
    Activate account when user clicks email link.
    """
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            return Response({"message": "Email verified successfully. You can now log in."})
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)