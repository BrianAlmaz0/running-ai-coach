from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RunViewSet, GoalViewSet, generate_plan, add_mock_runs, home

# Set up DRF router ViewSets
router = DefaultRouter()
router.register(r'runs', RunViewSet)
router.register(r'goals', GoalViewSet)

urlpatterns = [
    # API routes (e.g., /runs/, /goals/)
    path('api/', include(router.urls)),

    # Other endpoints
    path('generate-plan/', generate_plan, name='generate-plan'),
    path('add-mock-runs/', add_mock_runs, name='add-mock-runs'),

    # Home page
    path('', home, name='home'),
]
