from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, UserCreateViewSet, UserReceiveTokenViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

auth_urls = [
    path(
        'signup/',
        UserCreateViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'token/',
        UserReceiveTokenViewSet.as_view({'post': 'create'}),
        name='token'
    )
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls))
]
