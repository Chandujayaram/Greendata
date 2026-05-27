from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataSourceViewSet, EmissionRecordViewSet

router = DefaultRouter()
router.register(r'datasources', DataSourceViewSet)
router.register(r'emissions', EmissionRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]