from django.urls import path
from .views import UserProfileView, ActivateAccountView

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
]
