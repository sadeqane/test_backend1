from rest_framework.routers import DefaultRouter

from account.views import UserViewSet
from product.views import ProductViewSet

router = DefaultRouter()
router.register('',ProductViewSet,basename='products')

urlpatterns = router.urls


