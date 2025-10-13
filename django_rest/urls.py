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
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from books import views as books_views

router = routers.DefaultRouter()
# router.register(r'publishers', books_views.PublisherAPIView)
router.register(r'books', books_views.BookListCreateViewSet, basename='books')
# router.register(r'authors', books_views.AuthorsAPIView)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('api/v1/api-jwt-auth/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/api-jwt-auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # path('api/v1/api-token-auth/', obtain_auth_token, name='api-token-auth'),

    path('api/v1/testbasicauth/', auth_views.ProtectedDataView.as_view()),


    path('api/v1/', include(router.urls)),

    path('api/v1/login/', books_views.LoginView.as_view(), name='login'),
    path('api/v1/logout/', books_views.LogoutView.as_view(), name='logout'),

    # # схема OpenAPI
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    #
    # # Swagger UI
    # path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    #
    # # ReDoc UI (альтернатива Swagger)
    # path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
