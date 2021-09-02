from rest_framework import routers
from fakecsv import views


router = routers.DefaultRouter()
router.register(r'^schema', views.SchemaViewSet, basename='schema_view')
router.register(r'^schema/(?P<schema_id>\d+)/dataset', views.DatasetViewSet, basename='schema_view')

urlpatterns = router.urls
