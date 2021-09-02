from django.conf.urls import url
from django.conf import settings

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.contrib.auth import views
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
    url(r'^api/fakecsv/', include(('fakecsv.urls', 'fakecsv'))),
]


# spectacular
urlpatterns += [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
