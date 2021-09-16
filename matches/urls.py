from rest_framework.routers import DefaultRouter
from matches.views import MatchModelViewSet

router = DefaultRouter()
router.register(r'', MatchModelViewSet)

urlpatterns = router.urls
