from rest_framework.routers import DefaultRouter

from account.views import UserViewSet

router = DefaultRouter()
router.register('',UserViewSet,basename='users')

urlpatterns = router.urls
