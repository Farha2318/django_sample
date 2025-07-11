from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PortfolioViewSet, portfolio_summary, crypto_view

router = DefaultRouter()
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')

urlpatterns = router.urls + [
    path('', crypto_view, name='crypto_home'),
    path('portfolio-summary/', portfolio_summary, name='portfolio_summary'),
]
