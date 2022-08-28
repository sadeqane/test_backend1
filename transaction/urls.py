from django.urls import path

# router = DefaultRouter()
# router.register('',ProductViewSet,basename='products')
#
# urlpatterns = router.urls
from transaction.views import DepositView, BuyView, ResetDepositView

urlpatterns = [
    path('deposit/', DepositView.as_view(),name="deposit"),
    path('buy/', BuyView.as_view()),
    path('reset/', ResetDepositView.as_view()),
]
