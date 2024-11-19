from django.urls import path
from . import views

urlpatterns = [
    path('snippets/', views.snippet_list, name='snippet_list'),               # Endpoint for GET and POST snippets requests
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet_detail'),  # Endpoint for retrieving a snippet by ID
    path('users/', views.user_view, name='user_view'),                    # Endpoint for GET and POST user requests
]
