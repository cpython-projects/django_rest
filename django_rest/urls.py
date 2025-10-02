"""
URL configuration for django_rest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from books import views as books_views
from rest_framework import routers
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from test_auth import views as auth_views

from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt import views as jwt_views


router = routers.DefaultRouter()
# router.register(r'publishers', books_views.PublisherAPIView)
router.register(r'books', books_views.BookListCreateViewSet, basename='books')
# router.register(r'authors', books_views.AuthorsAPIView)



urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/v1/api-jwt-auth/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/api-jwt-auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # path('api/v1/api-token-auth/', obtain_auth_token, name='api-token-auth'),

    path('api/v1/testbasicauth/', auth_views.ProtectedDataView.as_view()),


    path('api/v1/', include(router.urls)),

    # схема OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc UI (альтернатива Swagger)
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
