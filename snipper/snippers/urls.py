from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # Endpoint for obtaining a new JWT token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint for refreshing the JWT token
    path('snippets/', views.snippet_list, name='snippet_list'),                    # Endpoint for GET and POST snippets requests
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),       # Endpoint for retrieving a snippet by ID
    path('users/', views.create_user, name='create_user'),                         # POST endpoint for creating users
    path('users/get/', views.get_user, name='get_user'),                           # GET endpoint for retrieving user info (requires JWT)
]
