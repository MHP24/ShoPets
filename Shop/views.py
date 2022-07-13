from django.http import JsonResponse
from django.shortcuts import render, redirect
from numpy import Infinity
from .models import Producto, PerfilUsuario, Factura, Carrito, Factura, DetalleFactura
from .forms  import ProductoForm, RegistrarUsuarioForm, EditarPerfilUsuarioForm, EditarUsuarioForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
# Create your views here.

def inicio(request):
    products = Producto.objects.filter(nomCategoria = "Gatos")
    return render(request, 'pages/index.html', {"list": products})

@csrf_exempt
def administrar_productos(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    data = {"list": Producto.objects.all()}
    return render(request, 'adminPages/products.html', data)

@csrf_exempt
def agregar_productos(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    form = ProductoForm(request.POST or None, request.FILES or None)
    if(request.method == 'POST'):
        if(form.is_valid()):
            Producto.objects.create(
                nomCategoria= request.POST.get("category"),
                nomProducto = request.POST.get("nomProducto"),
                descripcion = request.POST.get("descripcion"),
                precio = request.POST.get("precio"),
                porcDesctoSubscriptor = request.POST.get("porcDesctoSubscriptor"),
                porDesctoOferta = request.POST.get("porDesctoOferta"),
                urlImagenProducto = request.POST.get("urlImagenProducto")
            )
        return redirect('administrar_productos')
    return render(request, 'adminPages/addProduct.html', {'form': form})

@csrf_exempt
def editar_productos(request, idProd):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    producto = Producto.objects.get(idProducto=idProd)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if(request.method == 'POST'):
        if(form.is_valid()):
            form.save()
            Producto.objects.filter(idProducto=idProd).update(nomCategoria=request.POST.get("category"))
        return redirect('administrar_productos')
    return render(request, 'adminPages/editProduct.html', {'form': form, 'producto': producto})

@csrf_exempt
def eliminar_producto(request, idProd):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    producto = Producto.objects.get(idProducto=idProd)
    producto.delete()
    return redirect('administrar_productos')

#Administrador de stock 
@csrf_exempt
def administrar_stock(request):
    productos = Producto.objects.all()
    return render(request, 'adminPages/stock.html', {'productos': productos})

def editar_stock(request, idProd):
    producto = Producto.objects.get(idProducto = idProd)
    if(request.method == 'POST'):
        cantidad = request.POST.get("input__input--count")
        Producto.objects.filter(idProducto = idProd).update(stock = cantidad)
        return redirect(administrar_stock)
    return render(request, 'adminPages/editStock.html', {'producto': producto})

# Adminstrador de usuarios
@csrf_exempt
def administrar_usuarios(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    data = {"list": PerfilUsuario.objects.all()}
    return render(request, 'adminPages/users.html', data)

@csrf_exempt
def eliminar_usuario(request, userId):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    usuario = PerfilUsuario.objects.get(user=userId)
    usuario.delete()
    us = User.objects.get(id=userId)
    us.delete()
    return redirect(administrar_usuarios)

@csrf_exempt
def editar_usuario(request, userId):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    # Forms
    userProfile = PerfilUsuario.objects.get(user_id=userId)
    formPerfil = EditarPerfilUsuarioForm(request.POST or None, request.FILES or None, instance=userProfile)
    userData = User.objects.get(id=userId)
    formUser = EditarUsuarioForm(request.POST or None, request.FILES or None, instance=userData)
    suscriber = userProfile.esSubscriptor
    staff = userData.is_staff
    if request.method == 'POST':
        # Profile Data
        userRut = request.POST.get("rut")
        userAddress = request.POST.get("direccion")
        userImg = request.POST.get("urlImagenUsuario")
        userSuscription = request.POST.get("suscriber")
        suscriber = 'No'
        if(userSuscription == 'on'):
            suscriber = 'Si'

        #Auth User Data
        usName = request.POST.get("username")
        firstName = request.POST.get("first_name")
        lastName = request.POST.get("last_name")
        userEmail = request.POST.get("email")
        userPass = request.POST.get("input__input--password")
        userRole = request.POST.get("staffRole")
        staffRole = False
        if(userRole == 'on'):
            staffRole = True
        # Updates
        PerfilUsuario.objects.filter(id=userId).update(
            rut=userRut, 
            direccion=userAddress, 
            urlImagenUsuario=userImg, 
            esSubscriptor =suscriber
        )

        User.objects.filter(id=userId).update(
            username=usName,
            first_name=firstName,
            last_name=lastName,
            email=userEmail,
            password=userPass,
            is_staff=staffRole
        )
        return redirect('administrar_usuarios')
    return render(request, 'adminPages/editUser.html', 
    {'formPerfil': formPerfil, 'formUser': formUser, 
    'suscriber': suscriber, 'staff': staff, 'uId': userId})

############
@csrf_exempt
def administrar_historial(request):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    facturas = Factura.objects.all()
    return render(request, 'adminPages/history.html', {"facturas": facturas})
    
@csrf_exempt
def despachar(request, idFact):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    Factura.objects.filter(nroFactura=idFact).update(estadoActual='Despachado')
    return redirect(administrar_historial)

@csrf_exempt
def entregar(request, idFact):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    Factura.objects.filter(nroFactura=idFact).update(estadoActual='Entregado')
    return redirect(administrar_historial)

@csrf_exempt
def factura(request, idFact):
    if not (request.user.is_authenticated and request.user.is_staff):
        return redirect(inicio)
    factura = Factura.objects.get(nroFactura = idFact)
    detalleFactura = DetalleFactura.objects.filter(idFactura=factura)
    rutCliente = factura.idUsuario.rut
    nombreCliente = f'{factura.idUsuario.user.first_name} {factura.idUsuario.user.last_name}'
    fecha = factura.fecha
    etapa = factura.estadoActual
    return render(request, 'adminPages/bill.html', 
    {'factura': detalleFactura,
    'nFactura': idFact,
    'rut': rutCliente,
    'nombre': nombreCliente,
    'fecha': fecha,
    'etapa': etapa,
    'total': factura.montoTotal})

#### Client ####
def oferton(request):
    return render(request, 'pages/promotional.html')

def catalogo(request):
    data = {"list": Producto.objects.all()}
    return render(request, 'pages/catalog.html', data)

def buscar_producto(request):
    product = request.POST.get("search")
    searchResults = Producto.objects.filter(nomProducto__contains= product)
    return render(request, 'pages/catalog.html', {"list": searchResults})

def buscar_categoria(request, category):
    print(category)
    data = {"list": Producto.objects.filter(nomCategoria=category)}
    return render(request, 'pages/catalog.html', data)

def nosotros(request):
    return render(request, 'pages/about.html')

def producto(request, prodId):
    data = {"product": Producto.objects.get(idProducto=prodId), 
    "precioSubscriptor": int(Producto.objects.get(idProducto=prodId).precio * 0.95),
    "precioDescto": round(int(Producto.objects.get(idProducto=prodId).precio) * (1 - (int(Producto.objects.get(idProducto=prodId).porDesctoOferta))/100))}
    return render(request, 'pages/product.html', data)

def carro_compras(request):    
    if (not request.user.is_authenticated):
        return redirect(inicio)

    if(request.user.is_staff):
        return redirect(inicio)
    try:
        #Obtener usuario para instanciar
        usuario = PerfilUsuario.objects.get(id=request.user.id)
        #Obtener carro de compras del usuario que accede a la request
        carrito = Carrito.objects.filter(cliente = usuario)
        #Carro para reajustar segun descuentos si corresponde
        carroReajustado = []
        #Descuentos de subscriptor, sub total antes del descuento y total correspondiente con descuentos
        descuentoSubscriptor = 0
        subtotal = 0
        total = 0
        #En caso de cumplirse que es subscriptor el factor es de 0.05
        if(carrito[0].cliente.esSubscriptor == 'Si'):
            descuentoSubscriptor = 0.05
        
        #Recorrer productos en el carro de compras desde la bbdd para reajustarlos
        for producto in carrito:
            montoReajustado = round(producto.idproducto.precio * (1 - (descuentoSubscriptor + (producto.idproducto.porDesctoOferta/100))))
            carroReajustado.append({
                'imagen': producto.idproducto.urlImagenProducto,
                'categoria': producto.idproducto.nomCategoria, 
                'nombreProducto': producto.idproducto.nomProducto, 
                'precio': producto.idproducto.precio, 
                'descuentoSubscriptor': 5,
                'descuentoOferta': producto.idproducto.porDesctoOferta,
                'precioReajustado':montoReajustado,
                'idCarro': producto.idcarro
            })
            subtotal += producto.idproducto.precio
            total += montoReajustado
        return render(request, 'pages/shoppingCart.html', {'carro': carroReajustado, 'cantProductos': len(carroReajustado),
        'total': total, 'subTotal': subtotal, 'descuentos': (subtotal- total), 'subscriptor': carrito[0].cliente.esSubscriptor})
    except:
        return render(request, 'pages/shoppingCart.html', {'cantProductos': len(carroReajustado)})

def agregar_carro(request, prodId):
    if (not request.user.is_authenticated):
        return redirect(inicio)

    if(request.user.is_staff):
        return redirect(inicio)
    
    try:
        usuario = PerfilUsuario.objects.get(id=request.user.id)
        producto = Producto.objects.get(idProducto=prodId)
        Carrito.objects.create(cliente=usuario, idproducto=producto)
    except:
        return redirect(inicio)
    return redirect(catalogo)

def eliminar_carro(request, carroId):
    if (not request.user.is_authenticated):
        return redirect(inicio)

    if(request.user.is_staff):
        return redirect(inicio)

    try:
        Carrito.objects.filter(idcarro=carroId).delete()
        return redirect(carro_compras)
    except:
        return redirect(catalogo)

##### Funcion de compra #####
@csrf_exempt
def comprar(request):
    if (not request.user.is_authenticated):
        return redirect(inicio)

    if(request.user.is_staff):
        return redirect(inicio)
    #Obtener usuario asociado a la compra y su carro de compra actual...
    usuario = PerfilUsuario.objects.get(id=request.user.id)
    carrito = Carrito.objects.filter(cliente = usuario)

    #Revisión de stock antes de realizar las compras, en caso de que alguno de los productos en el carro no se 
    #encuentre disponible no dejará realizar la transacción
    cantidadProductos = {}
    for producto in carrito:
        if(producto.idproducto.idProducto in cantidadProductos):
            cantidadProductos[producto.idproducto.idProducto] = cantidadProductos[producto.idproducto.idProducto] + 1
        else:
            cantidadProductos[producto.idproducto.idProducto] = 1

    #Validamos de que si la cantidad de productos obtenidos dentro de cantidadProductos es mayor al stock disponible
    #no realice la compra
    for producto in cantidadProductos:
        if(cantidadProductos[producto] > Producto.objects.get(idProducto = producto).stock):
            return redirect(carro_compras)

    #En caso de no retornar la compra se realizará de manera exítosa tal que recalculará el stock
    #y procederá a generar la factura
    for producto in cantidadProductos:
        Producto.objects.filter(idProducto = producto).update(
            stock = (Producto.objects.get(idProducto = producto).stock - cantidadProductos[producto]))

    #Para registrar la compra se debe efectuar la insercion de datos en la tabla de DetalleFactura y Factura
    #Subtotal (Sin descuentos) Total (Descuentos)
    subTotal = 0
    total = 0
    #Descuento subscriptor (FACTOR Inicial)
    desctoSub = 0

    if(carrito[0].cliente.esSubscriptor == 'Si'):
        desctoSub = 0.05
    for producto in carrito:
        montoReajustado = round(producto.idproducto.precio * (1 - (desctoSub + (producto.idproducto.porDesctoOferta/100))))
        total += montoReajustado
        subTotal += producto.idproducto.precio
    #Insercion en tabla Factura con el estado actual de la compra el cual por defecto será En Bodega
    Factura.objects.create(idUsuario=usuario, montoTotal=total, estadoActual='En Bodega')

    #Una vez creada la factura se debe obtener el identificador de esta,
    #lo que se obtiene a partir del valor maximo de las facturas que posee dicho cliente
    facturas = Factura.objects.filter(idUsuario=usuario)
    nroFact = -Infinity
    for f in facturas:
        if(f.nroFactura > nroFact):
            nroFact = f.nroFactura

    #Traer data dellada de la factura obtenida para instanciar
    factura = Factura.objects.get(nroFactura=nroFact)
    #Recorrer carro en bbdd e insertar los productos como detalle
    for producto in carrito:
        subTotal = producto.idproducto.precio
        total = round(producto.idproducto.precio * (1 - (desctoSub + (producto.idproducto.porDesctoOferta/100))))
        DetalleFactura.objects.create(
        idFactura=factura,
        idProducto=producto.idproducto,
        porcDesctoSubscriptor=(desctoSub * 100),
        porDesctoOferta=producto.idproducto.porDesctoOferta,
        subTotal=subTotal,
        total=total)

    #Eliminar todas las cosas del carro de compras del usuario
    Carrito.objects.filter(cliente = usuario).delete()
    return redirect(perfil)

@csrf_exempt
def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect(inicio)
    data = {"mesg": ""}
    if(request.method == 'POST'):
        usname = request.POST.get("username")
        contrasena = request.POST.get("contrasena")
        user = authenticate(username=usname, password=contrasena)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(inicio)
        else:
            data["mesg"] = "¡La cuenta o la password no son correctos!"
    return render(request, 'pages/login.html', data)

@csrf_exempt
def registrarse(request):
    if request.user.is_authenticated:
        return redirect(inicio)
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            rut = request.POST.get("rut")
            direccion = request.POST.get("direccion")
            imgUser = request.POST.get("userImg")
            sub = 'No'
            suscripcion = request.POST.get("suscripcion")
            if(suscripcion == 'on'):
                sub = 'Si'
            PerfilUsuario.objects.update_or_create(user=user, rut=rut, direccion=direccion, esSubscriptor=sub, urlImagenUsuario=imgUser)
            return redirect(iniciar_sesion)
    form = RegistrarUsuarioForm()
    return render(request, 'pages/register.html', context={'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect(inicio)

@csrf_exempt
def perfil(request):
    if not request.user.is_authenticated:
        return redirect(inicio)
    userId = request.user.id
    user = User.objects.get(id=userId)
    perfil = PerfilUsuario.objects.get(user_id=userId)

    tipoUsuario = 'Cliente'
    if(perfil.esSubscriptor == 'Si'):
        tipoUsuario = 'Miembro'

    facturas = Factura.objects.filter(idUsuario = perfil)
    return render(request, 'pages/profile.html', {"perfil": perfil, "user": user, 
    "tipoUsuario": tipoUsuario, 'facturas': facturas})

@csrf_exempt
def editar_perfil(request):
    if not request.user.is_authenticated:
        return redirect(inicio)
    userId = request.user.id
    userProfile = PerfilUsuario.objects.get(user_id=userId)
    formPerfil = EditarPerfilUsuarioForm(request.POST or None, request.FILES or None, instance=userProfile)
    userData = User.objects.get(id=userId)
    formUser = EditarUsuarioForm(request.POST or None, request.FILES or None, instance=userData)
    suscriber = userProfile.esSubscriptor
    if request.method == 'POST':
        # Profile Data
        userRut = request.POST.get("rut")
        userAddress = request.POST.get("direccion")
        userImg = request.POST.get("urlImagenUsuario")
        userSuscription = request.POST.get("suscriber")
        suscriber = 'No'
        if(userSuscription == 'on'):
            suscriber = 'Si'

        #Auth User Data
        usName = request.POST.get("username")
        firstName = request.POST.get("first_name")
        lastName = request.POST.get("last_name")
        userEmail = request.POST.get("email")
        # Updates
        PerfilUsuario.objects.filter(id=userId).update(
            rut=userRut, 
            direccion=userAddress, 
            urlImagenUsuario=userImg, 
            esSubscriptor =suscriber
        )

        User.objects.filter(id=userId).update(
            username=usName,
            first_name=firstName,
            last_name=lastName,
            email=userEmail,
        )
        return redirect('inicio')
    return render(request, 'pages/profile-edit.html', 
    {'formPerfil': formPerfil, 'formUser': formUser, 
    'suscriber': suscriber})

@csrf_exempt
def compra(request, idFact):
    if not (request.user.is_authenticated):
        return redirect(inicio)
    factura = Factura.objects.get(nroFactura = idFact)
    detalleFactura = DetalleFactura.objects.filter(idFactura=factura)
    rutCliente = factura.idUsuario.rut
    nombreCliente = f'{factura.idUsuario.user.first_name} {factura.idUsuario.user.last_name}'
    fecha = factura.fecha
    etapa = factura.estadoActual
    return render(request, 'pages/tracking.html', 
    {'factura': detalleFactura,
    'nFactura': idFact,
    'rut': rutCliente,
    'nombre': nombreCliente,
    'fecha': fecha,
    'etapa': etapa,
    'total': factura.montoTotal})


# API Rest
@api_view(['POST'])
def logg(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("Usuario invalido")

    pwd_valid = check_password(password,user.password)

    if not pwd_valid:
        return Response("Contraseña invalida")

    token = Token.objects.create(user=user)
    return Response(token.key)

def poblar_db(request):
    Producto.objects.create(nomCategoria="Perros", nomProducto='Saco DogChow', descripcion="Saco de comida para perro 1kg", precio=25000, porcDesctoSubscriptor=5, porDesctoOferta=2, urlImagenProducto='https://bodegadispal.cl/wp-content/uploads/2021/06/765.png')
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Saco Whiskas', descripcion="Saco de comida para gato 1kg", precio=15000, porcDesctoSubscriptor=5, porDesctoOferta=3, urlImagenProducto='https://www.whiskas.cl/wp-content/uploads/2019/12/Hogare%C3%B1os-Adulto-e1581093305603.jpg')
    Producto.objects.create(nomCategoria="Perros", nomProducto='Collar RuffWear', descripcion="Collar para perros", precio=25000, porcDesctoSubscriptor=5, porDesctoOferta=1, urlImagenProducto='https://www.amigales.cl/pub/media/catalog/product/cache/c687aa7517cf01e65c009f6943c2b1e9/t/o/top-rope-collar-sunset_1_3.jpg')
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Cat Love Super Mix Arena', precio=19990, porcDesctoSubscriptor=5, porDesctoOferta= 2, descripcion= "Cat Love Arena Super Mix contiene bentonita de sodio lo que la hace una arena excelente aglutinando, perfecta controlando olores y de muy fácil limpieza.", urlImagenProducto="https://dojiw2m9tvv09.cloudfront.net/11787/product/supermix-arenasanitaria18kg3989.jpg")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Royal Canin Alimento Húmedo Gatitos', precio=2190, porcDesctoSubscriptor=5, porDesctoOferta= 2, descripcion= "Royal Canin Alimento Húmedo Gatitos es una deliciosa combinación de sabores de pescado y atún, en un suave y agradable paté que tendrán a tu gato esperando con impaciencia la hora de comer todos los días.", urlImagenProducto="https://cdn.royalcanin-weshare-online.io/4lbvLnIBBKJuub5qMHG7/v5/cl-l-producto-kitten-pouch-feline-health-nutrition-humedo")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Bravery Chicken Adult Cat', precio=39990, porcDesctoSubscriptor=5, porDesctoOferta= 3, descripcion= "Bravery Adult Cat Chicken es un alimento premium para gatos desde 1 año de edad. Su fórmula es libre de grano, monoproteico e hipoalergénico. Hecho con productos 100% naturales a base de proteínas y antioxidantes. Entrega todos los nutrientes necesarios para mantener una vida sana y activa.", urlImagenProducto="https://dojiw2m9tvv09.cloudfront.net/11787/product/braverychickenadultcat0194.jpg")
    Producto.objects.create(nomCategoria="Perros", nomProducto='Dispensador Snail', precio=23900, porcDesctoSubscriptor=5, porDesctoOferta= 4, descripcion= "Dispensador de agua y comida con diseño innovador para perros.", urlImagenProducto="https://spzcdn01.akamaized.net/assets/uploads/productos/sliders/d5cfc-dispensador-snail-002_thumbs.jpg")
    Producto.objects.create(nomCategoria="Perros", nomProducto='Plato Crock Metálico', precio=15192, porcDesctoSubscriptor=5, porDesctoOferta= 2, descripcion= "Cuenco de acero inoxidable para perros.", urlImagenProducto="https://s.cornershopapp.com/product-images/5815397.jpg?versionId=eTajKuCyfBhsXg.4iGeerCtc6Olf3OgV")
    Producto.objects.create(nomCategoria="Perros", nomProducto='Zeedog Arnés Ajustable Ella', precio=26990, porcDesctoSubscriptor=5, porDesctoOferta= 4, descripcion= "Arnés de pecho de malla ajustable y transpirable para perro.", urlImagenProducto="https://s3.us-east-2.amazonaws.com/media-attachments.ambar.pet/wp-content/uploads/2022/02/04041459/14510-ella-1_air_mesh_ajustavel.jpg")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Oxyfresh Shampoo Para Mascotas', precio=13900, porcDesctoSubscriptor=5, porDesctoOferta= 1, descripcion= "El shampoo para mascotas Oxyfresh es definitivamente el mejor que vas a encontrar. Diseñamos nuestra fórmula con pH balanceado para apoyar y calmar la delicada piel de las mascotas que sufren de alergia, ya que es clave para la salud general de las mascotas. Es crucial cuidar su defensa natural contra descamamiento, la picazón, la sequedad y el olor.", urlImagenProducto="https://felinus.cl/1234-large_default/oxyfresh-shampoo-para-mascotas.jpg")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Leonardo Quality Selection Kitten', precio=37900, porcDesctoSubscriptor=5, porDesctoOferta= 2, descripcion= "Alimento húmedo completo para gatitos.", urlImagenProducto="https://http2.mlstatic.com/D_NQ_NP_763510-MLA48462210776_122021-O.webp")
    Producto.objects.create(nomCategoria="Perros", nomProducto='Desparasitante Bravecto', precio=41592, porcDesctoSubscriptor=5, porDesctoOferta= 3, descripcion= "Comprimido masticable contra pulgas y garrapatas en perros.", urlImagenProducto="https://www.amigales.cl/pub/media/catalog/product/cache/c687aa7517cf01e65c009f6943c2b1e9/a/n/antiparasitario_bravecto_perros_01.jpg")
    Producto.objects.create(nomCategoria="Gatos", nomProducto='Churu De Atún Con Ostiones', precio=13450, porcDesctoSubscriptor=5, porDesctoOferta= 4, descripcion= "Alimento cremoso e irresistible para gatos sabor atún con ostiones.", urlImagenProducto="https://felinus.cl/915-large_default/inaba-churu-sabor-atun-con-ostiones.jpg")
    return redirect(inicio)