from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
urlpatterns = [
    path('create_product', views.post_products.as_view(), name="post_products"),
    path('update_product', views.put_products.as_view(), name="put_products"),
    path('get_products/<int:id>', views.product_get_by_id, name="product_get_by_id"),
    path('get_products', views.product_get, name='product_get'),
    path('delete_product/<id>', views.product_delete, name="product_delete"),
    path('login', views.login, name='login')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)