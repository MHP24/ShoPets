from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('administrar_productos', views.administrar_productos,  name="administrar_productos"),
    path('administrar_stock', views.administrar_stock,  name="administrar_stock"),
    path('editar_stock/<idProd>', views.editar_stock,  name="editar_stock"),
    path('', views.inicio, name="inicio"),
    path('catalogo', views.catalogo, name="catalogo"),
    path('oferton', views.oferton, name="oferton"),
    path('catalogo/<category>', views.buscar_categoria, name="catalogo"),
    path('buscar_producto', views.buscar_producto, name="buscar_producto"),
    path('nosotros', views.nosotros, name="nosotros"),
    path('producto/<prodId>', views.producto, name="producto"),
    path('agregar_carro/<prodId>', views.agregar_carro, name="agregar_carro"),
    path('eliminar_carro/<carroId>', views.eliminar_carro, name="eliminar_carro"),
    path('carrito', views.carro_compras, name="carrito"),
    path('comprar', views.comprar, name="comprar"),
    path('perfil', views.perfil, name="perfil"),
    path('editar_perfil', views.editar_perfil, name="editar_perfil"),
    path('agregar_productos', views.agregar_productos, name="agregar_productos"),
    path('editar_productos/<idProd>', views.editar_productos, name="editar_productos"),
    path('eliminar_producto/<idProd>', views.eliminar_producto, name="eliminar_producto"),
    path('editar_usuario<userId>', views.editar_usuario, name="editar_usuario"),
    path('administrar_usuarios', views.administrar_usuarios, name="administrar_usuarios"),
    path('eliminar_usuario/<userId>', views.eliminar_usuario, name="eliminar_usuario"),
    path('administrar_historial', views.administrar_historial, name="administrar_historial"),
    path('despachar/<idFact>', views.despachar, name="despachar"),
    path('entregar/<idFact>', views.entregar, name="entregar"),
    path('factura/<idFact>', views.factura, name="factura"),
    path('compra/<idFact>', views.compra, name="compra"),
    path('registrarse', views.registrarse, name="registrarse"),
    path('iniciar_sesion', views.iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion', views.cerrar_sesion, name="cerrar_sesion"),
    path('poblar_db', views.poblar_db, name="poblar_db")
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)