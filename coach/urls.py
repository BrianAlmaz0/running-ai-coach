from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RunViewSet, GoalViewSet

router = DefaultRouter()
router.register(r'runs', RunViewSet)
router.register(r'goals', GoalViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
