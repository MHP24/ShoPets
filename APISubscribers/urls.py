from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
urlpatterns = [
    path('subscribers', views.SubscribersAPI.as_view(), name="subscribers"),
    path('subscribers/<int:idu>', views.SubscribersAPI.as_view(), name="specify_subscriber"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)