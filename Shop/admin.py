from django.contrib import admin
from .models import Producto, PerfilUsuario, Factura, Carrito, DetalleFactura
# Register your models here.
admin.site.register(Producto)
admin.site.register(PerfilUsuario)
admin.site.register(Factura)
admin.site.register(Carrito)
admin.site.register(DetalleFactura)
