from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from .forms import LoginForm, RegisterForm, changePhoto, comentarioForm
from django.contrib.auth.models import User
from .models import Item,Alimentador, Comentario, Users, Voto
import urllib.request
from xml.sax import make_parser
from .parseyt import YTHandler
from .parseflickr import FlickrHandler
from .parselastfm import LastfmHandler
from .apikeys import LASTFM_APIKEY
from unidecode import unidecode
from django.core import serializers


def index(request):
    paginaPrincipal = True
    form = LoginForm()

    alimentadoresYT = Alimentador.objects.filter(pagPrincipal=True,type="youtube")
    alimentadoresFR = Alimentador.objects.filter(pagPrincipal=True,type="flickr")
    alimentadoresLF = Alimentador.objects.filter(pagPrincipal=True,type="lastfm")

    items =Item.objects.all()
    for item in items:
        item.votosTotales = item.votosPositivos - item.votosNegativos
        item.save()

    itemsOrdenados = Item.objects.all().order_by('-votosTotales')[:10]

    context = {'paginaPrincipal': paginaPrincipal,
                'form': form,
               'alimentadoresYT': alimentadoresYT,
               'alimentadoresFR': alimentadoresFR,
               'alimentadoresLF': alimentadoresLF,
               'top10': itemsOrdenados}

    user = request.user.username
    if user:
        try:
            user = Users.objects.get(username=user)
        except Users.DoesNotExist:
            user = Users(username=user)
            user.save()
        votos = Voto.objects.filter(usuario=user).order_by('-id')[:5]
        context['itemsvotados'] = votos

    if request.method == "POST":
        action = request.POST['action']
        if action == "youtube":
            idchannel = request.POST['idyoutube']
            redireccion = "/MisCosas/youtube/" + idchannel
            return HttpResponseRedirect(redireccion)

        elif action == "flickr":
            idtag = request.POST['idflickr']
            idtag = unidecode(idtag)
            redireccion = "/MisCosas/flickr/" + idtag
            return redirect(redireccion)

        elif action == "lastfm":
            artist = request.POST['artistlast']
            artist = unidecode(artist)
            redireccion = "/MisCosas/lastfm/" + artist
            return redirect(redireccion)


    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'MisCosas/index.xml', context, content_type='text/xml')
        if format == 'json':
            list = [*itemsOrdenados, *alimentadoresYT, *alimentadoresFR,*alimentadoresLF]
            if user:
                list = [*itemsOrdenados,*votos, *alimentadoresYT, *alimentadoresFR, *alimentadoresLF]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")
    return render(request, 'MisCosas/index.html', context)

def alimentadores(request):
    form=LoginForm
    paginaAlimentadores = True
    try:
        alimentadoresYT = Alimentador.objects.filter(type="youtube")
        alimentadoresFR = Alimentador.objects.filter(type="flickr")
        alimentadoresLF = Alimentador.objects.filter(type="lastfm")

        context = {'alimentadoryoutube': alimentadoresYT,
                   'alimentadoresflickr':alimentadoresFR,
                   'alimentadoreslast':alimentadoresLF,
                   'paginaAlimentadores':paginaAlimentadores,
                   'form': form}

    except Alimentador.DoesNotExist:
        context = {}

    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'MisCosas/alimentadores.xml', context, content_type='text/xml')
        if format == 'json':
            list = [*alimentadoresYT, *alimentadoresFR, *alimentadoresLF]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")

    return render(request,'MisCosas/alimentadores.html',context)

def borrarprincipal(request, llave, llave1,llave2 ):
    if llave == 'flickr':
        llaveTraducida = llave1.replace(" ","").lower()
        a = Alimentador.objects.get(alimentadorId=llaveTraducida)
    else:
        a = Alimentador.objects.get(alimentadorId=llave1)

    a.pagPrincipal = not a.pagPrincipal
    a.save()
    if llave2 == "paginaPrincipal":
        redireccion = "/MisCosas/"
    elif llave2  == "paginaAlimentador":
        redireccion = "/MisCosas/"+ llave + "/" + llave1

    return redirect(redireccion)

def processalimentador(request, llave1, llave2):
    Parser = make_parser()
    if llave1 == 'youtube':
        Parser.setContentHandler(YTHandler())
        url = 'https://www.youtube.com/feeds/videos.xml?channel_id=' \
            + llave2

    if llave1 == 'flickr':
        llave2 = llave2.replace(" ", "%20") # Convierto los espacios en %20 para que se pueda parsear
        Parser.setContentHandler(FlickrHandler())
        url = 'https://www.flickr.com/services/feeds/photos_public.gne?tags=' \
              + llave2
        llave2 = llave2.replace("%20", "").lower() # convierto el título en la llave que siempre se hace quitando los espacios y en minuscula

    if llave1 == 'lastfm':
        llavetraducida = llave2.replace(" ", "%20")
        Parser.setContentHandler(LastfmHandler())
        url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=' + llavetraducida + '&api_key=' + LASTFM_APIKEY

    try:
        xmlStream = urllib.request.urlopen(url)
        Parser.parse(xmlStream)
    except:
        return render(request, 'MisCosas/404.html', {})
    try:
        a = Alimentador.objects.get(alimentadorId=llave2)
    except:
        return render(request, 'MisCosas/404.html', {})

    items = Item.objects.filter(alimentador=a)

    for item in items:
        item.votosTotales = item.votosPositivos - item.votosNegativos
        item.save()

    form= LoginForm();
    context = {'contentList': items,
               'alimentador': a,
               'form':form}

    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'MisCosas/alimentador.xml', context, content_type='text/xml')
        if format == 'json':
            list = [a, *items]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")

    return render(request, 'MisCosas/alimentador.html', context)

def processitem(request, llave,llave1, llave2):

    a = Alimentador.objects.get(alimentadorId=llave1)
    i = Item.objects.get(itemId=llave2)
    form = LoginForm()

    context = {'alimentador': a,
               'item': i,
               'form': form}

    user = request.user.username
    if user:
        user = Users.objects.get(username=user)
        context['users'] = user
        context['form2'] = comentarioForm()
        form = comentarioForm(request.POST, request.FILES)
        if form.is_valid():
            cuerpo = form.cleaned_data['comentario']
            imagen = form.cleaned_data['imagen']
            c = Comentario(usuario=user, fecha=timezone.now(), cuerpo=cuerpo, item=i, imagen=imagen)
            c.save()
        try:
            voto = Voto.objects.get(usuario=user, item=i)
            context['voto'] = voto
        except Voto.DoesNotExist:
            print("no votes")

    try:
        comments = Comentario.objects.filter(item__itemId=llave2)
        context['comment'] = comments
    except Comentario.DoesNotExist:
        print("No Comments")

    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'MisCosas/item.xml', context, content_type='text/xml')
        if format == 'json':
            list = [a, i]
            if user:
                list = [a, i,*comments]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")
    return render(request, 'MisCosas/item.html',context)

def gestionvotos(request,llave, llave1,llave2,llave3):
    i = Item.objects.get(itemId=llave2)
    name = request.user.username
    if name:
        action = request.POST.get('action', None)
        u = Users.objects.get(username=name)

        if action == "votopositivo":
            try:
                v = Voto.objects.get(usuario=u, item=i)
                if v.estado == "estadonegativo":
                    i.votosPositivos = i.votosPositivos + 1
                    i.votosNegativos = i.votosNegativos - 1
                    i.save()
                v.estado = "estadopositivo"
                v.save()
            except Voto.DoesNotExist:
                i.votosPositivos = i.votosPositivos + 1
                i.save()
                v = Voto(usuario=u, item=i, estado="estadopositivo")
                v.save()

        elif action =="votonegativo":
            try:
                v = Voto.objects.get(usuario=u, item=i)
                if v.estado == "estadopositivo":
                    i.votosPositivos = i.votosPositivos - 1
                    i.votosNegativos = i.votosNegativos + 1
                    i.save()
                v.estado = "estadonegativo"
                v.save()
            except Voto.DoesNotExist:
                i.votosNegativos = i.votosNegativos + 1
                i.save()
                v = Voto(usuario=u, item=i, estado="estadonegativo")
                v.save()

        a = Alimentador.objects.get(alimentadorId=llave1)
        items = Item.objects.filter(alimentador=a)
        votospos = 0
        votosne = 0
        for votos in items:
            votospos = votos.votosPositivos + votospos
            votosne = votos.votosNegativos + votosne

        puntuacionAlimentador = votospos - votosne
        a.puntuacion = puntuacionAlimentador
        a.save()
    if llave3 == 'paginaPrincipal':
        redireccion = "/MisCosas/"
    elif llave3 == 'paginaItem':
        redireccion  = "/MisCosas" + "/" + llave + "/" + llave1 + "/" + llave2

    return redirect(redireccion)

def users(request):
    paginaUsuarios = True
    form = LoginForm()
    users = Users.objects.all()

    context = {'users':users,
               'paginaUsuarios':paginaUsuarios,
               'form': form}

    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'MisCosas/users.xml', context, content_type='text/xml')
        if format == 'json':
            list = [*users]
            lista = serializers.serialize('json', list, fields=['username','email'])
            return HttpResponse(lista, content_type="application/json")
    return render(request,'MisCosas/users.html', context)


def user(request, llave):
    users = Users.objects.get(username = llave)

    itemsComentados = Comentario.objects.filter(usuario = users)
    itemsVotados = Voto.objects.filter(usuario=users)

    form = LoginForm()
    form2 = changePhoto()
    context = {'users': users,
               'form': form,
               'itemscomentados': itemsComentados,
                'itemsvotados': itemsVotados,
               'form2':form2}

    if users.username == request.user.username:
        sameuser = True
        context['sameuser'] = sameuser

    if request.method == "POST":
        if 'tamañoletra' in request.POST:
            tamañoletra= request.POST['tamañoletra']
            if tamañoletra == "grande":
                letra = "2rem"
            elif tamañoletra == "mediana":
                letra = "1.1rem"
            elif  tamañoletra == "pequeña":
                letra = "0.5rem"

            users.tamañoletra = letra

        elif 'estilo' in request.POST:
            estilo = request.POST['estilo']
            if estilo == "Oscuro":
                fondo = "black"
            elif estilo == "Ligero":
                fondo = "white"

            users.estilo = fondo

        else:
            form2 = changePhoto(request.POST, request.FILES)
            if form2.is_valid():
                image = form2.cleaned_data['image']
                users.image = image

        users.save()

    if request.method == "GET":
        format = request.GET.get('format')
        if format == 'xml':
            return render(request, 'MisCosas/perfil.xml', context, content_type='text/xml')
        if format == 'json':
            list = [users,*itemsComentados,*itemsVotados]
            lista = serializers.serialize('json', list)
            return HttpResponse(lista, content_type="application/json")
    return render(request, 'MisCosas/perfil.html', context)


def register(request):
    form = RegisterForm()
    context = {'form': form}
    if request.method == "POST":
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data['Username']
            email = form.cleaned_data['Email']
            contraseña = form.cleaned_data['Password']
            image = form.cleaned_data['image']
            try:
                superUser = User.objects.get(username=nombre)
                context['error'] = 'Usuario existente, pruebe otro'
                return render(request, 'MisCosas/register.html', context)
            except User.DoesNotExist:
                try:
                    user = Users.objects.get(username=nombre)
                    context['error'] = 'Usuario existente, pruebe otro'
                    return render(request, 'MisCosas/register.html', context)
                except Users.DoesNotExist:
                    u = Users(username=nombre, email=email, password=contraseña,image = image)
                    u.save()
                    user = User.objects.create_user(username=nombre, email=email, password=contraseña)
                    user.save()
                    if user is not None:
                        login(request,user)
                    return redirect('index')

    return render(request, 'MisCosas/register.html', context)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['Username']
            contraseña = form.cleaned_data['Password']
            user = authenticate(request, username=nombre, password=contraseña)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

def informacion(request):
    form = LoginForm()
    pagInformacion = True
    context = {'pagInformacion':pagInformacion,
               'form':form}
    return render(request, 'MisCosas/informacion.html', context)

def css(request):
    context = {}
    try:
        users = Users.objects.get(username=request.user.username)
        context['users'] = users
    except Users.DoesNotExist:
        print("")

    return render(request, 'MisCosas/base.css', context, content_type='text/css')

def page_not_found(request,exception):
    return render(request, 'MisCosas/404.html', {})