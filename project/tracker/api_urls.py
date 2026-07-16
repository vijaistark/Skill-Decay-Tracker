from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import api_views

router = DefaultRouter()
router.register('skills', api_views.SkillViewSet, basename='skill')
router.register('logs', api_views.PracticeLogViewSet, basename='practicelog')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', api_views.DashboardViewSet.as_view({'get': 'stats'}), name='api-dashboard'),
]
