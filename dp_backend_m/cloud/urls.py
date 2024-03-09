from cloud.views import UsersView, UserView, UserUpdateView, UserDeleteView, FileCreateView, FileUpdateView, \
    FileDeleteView, FreefileView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('users/', UsersView.as_view()),
    path('users/<int:pk>/', UserView.as_view()),
    path('users/update/<int:pk>/', UserUpdateView.as_view()),
    path('users/delete/<int:pk>/', UserDeleteView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('files/', FileCreateView.as_view()),
    path('files/freefile/<int:pk>/', FreefileView.as_view()),
    path('files/update/<int:pk>/', FileUpdateView.as_view()),
    path('files/delete/<int:pk>/', FileDeleteView.as_view()),
    path('download/<str:url>/', FreefileView.as_view()),
]