
from django.test import TestCase, SimpleTestCase
import tempfile
from . import views
from .forms import LoginForm, RegisterForm, comentarioForm

#TEST  VIEWS
class TestRequest(TestCase):
    #INDEX
    def test_index_get(self):
        response = self.client.get('/MisCosas/')
        self.assertEqual(response.resolver_match.func, views.index)
        self.assertEqual(response.status_code, 200)

    def test_index_post_flickr(self):
        response = self.client.post('/MisCosas/flickr/Madrid')
        self.assertEqual(response.resolver_match.func, views.processalimentador)
        self.assertEqual(response.status_code, 200)

    def test_index_post_youtube(self):
        response = self.client.post('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg')
        self.assertEqual(response.resolver_match.func, views.processalimentador)
        self.assertEqual(response.status_code, 200)

    def test_index_post_lastfm(self):
        response = self.client.post('/MisCosas/lastfm/izal')
        self.assertEqual(response.resolver_match.func, views.processalimentador)
        self.assertEqual(response.status_code, 200)

    #ALIMENTADORES
    def test_alimentadores_get_post(self):
        response1 = self.client.get('/MisCosas/alimentadores/')
        response2 = self.client.post('/MisCosas/alimentadores/')
        self.assertEqual(response1.resolver_match.func, views.alimentadores)
        self.assertEqual(response2.resolver_match.func, views.alimentadores)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    # BORRAR ALIMENTADORES
    def test_borrarprincipal_get_post_youtube_paginaprincipal(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="UC300utwSVAYOoRLEqmsprfg", type="youtube")
        a.save()
        response1 = self.client.get('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg/paginaPrincipal/De-Seleccionar')
        response2 = self.client.post('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg/paginaPrincipal/De-Seleccionar')
        self.assertEqual(response1.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response2.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    def test_borrarprincipal_get_post_flickr_paginaprincipal(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="madrid", type="flickr")
        a.save()
        response1 = self.client.get('/MisCosas/flickr/Madrid/paginaPrincipal/De-Seleccionar')
        response2 = self.client.post('/MisCosas/flickr/Madrid/paginaPrincipal/De-Seleccionar')
        self.assertEqual(response1.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response2.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    def test_borrarprincipal_get_post_lastfm_paginaprincipal(self):
        from .models import Alimentador
        a = Alimentador(alimentadorId="Izal", type="lastfm")
        a.save()
        response1 = self.client.get('/MisCosas/lastfm/Izal/paginaPrincipal/De-Seleccionar')
        response2 = self.client.post('/MisCosas/lastfm/Izal/paginaPrincipal/De-Seleccionar')
        self.assertEqual(response1.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response2.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    def test_borrarprincipal_get_post_youtube_paginaalimentador(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="UC300utwSVAYOoRLEqmsprfg", type="youtube")
        a.save()
        response1 = self.client.get('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg/paginaAlimentador/De-Seleccionar')
        response2 = self.client.post('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg/paginaAlimentador/De-Seleccionar')
        self.assertEqual(response1.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response2.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    def test_borrarprincipal_get_post_flickr_paginaalimentador(self):
        from .models import Alimentador
        a = Alimentador(alimentadorId="madrid", nombre='Madrid', type="flickr")
        a.save()
        response1 = self.client.get('/MisCosas/flickr/Madrid/paginaAlimentador/De-Seleccionar')
        response2 = self.client.post('/MisCosas/flickr/Madrid/paginaAlimentador/De-Seleccionar')
        self.assertEqual(response1.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response2.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    def test_borrarprincipal_get_post_lastfm_paginaalimentador(self):
        from .models import Alimentador
        a = Alimentador(alimentadorId="Izal", type="lastfm")
        a.save()
        response1 = self.client.get('/MisCosas/lastfm/Izal/paginaAlimentador/De-Seleccionar')
        response2 = self.client.post('/MisCosas/lastfm/Izal/paginaAlimentador/De-Seleccionar')
        self.assertEqual(response1.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response2.resolver_match.func, views.borrarprincipal)
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)

    #ALIMENTADOR

    def test_processalimentador_get_post_youtube(self):
        response1 = self.client.get('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg')
        response2 = self.client.post('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg')
        self.assertEqual(response1.resolver_match.func, views.processalimentador)
        self.assertEqual(response2.resolver_match.func, views.processalimentador)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_processalimentador_get_post_flickr(self):
        response1 = self.client.get('/MisCosas/flickr/Madrid')
        response2 = self.client.post('/MisCosas/flickr/Madrid')
        self.assertEqual(response1.resolver_match.func, views.processalimentador)
        self.assertEqual(response2.resolver_match.func, views.processalimentador)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_processalimentador_get_post_lastfm(self):
        response1 = self.client.get('/MisCosas/lastfm/Izal')
        response2 = self.client.post('/MisCosas/lastfm/Izal')
        self.assertEqual(response1.resolver_match.func, views.processalimentador)
        self.assertEqual(response2.resolver_match.func, views.processalimentador)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    #ITEM
    def test_processitem_get_post_youtube(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="UC300utwSVAYOoRLEqmsprfg", type="youtube")
        a.save()
        i = Item(itemId = "HZOodD84MR8")
        i.save()
        response1 = self.client.get('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg/HZOodD84MR8')
        response2 = self.client.post('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg/HZOodD84MR8')
        self.assertEqual(response1.resolver_match.func, views.processitem)
        self.assertEqual(response2.resolver_match.func, views.processitem)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_processitem_get_post_flickr(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="Madrid", type="flickr")
        a.save()
        i = Item(itemId="49915596093")
        i.save()
        response1 = self.client.get('/MisCosas/flickr/Madrid/49915596093')
        response2 = self.client.post('/MisCosas/flickr/Madrid/49915596093')
        self.assertEqual(response1.resolver_match.func, views.processitem)
        self.assertEqual(response2.resolver_match.func, views.processitem)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_processitem_get_post_lastfm(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="Izal", type="lastfm")
        a.save()
        i = Item(itemId="copacabana")
        i.save()
        response1 = self.client.get('/MisCosas/lastfm/Izal/copacabana')
        response2 = self.client.post('/MisCosas/lastfm/Izal/copacabana')
        self.assertEqual(response1.resolver_match.func, views.processitem)
        self.assertEqual(response2.resolver_match.func, views.processitem)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    #GESTION VOTOS
    def test_gestionvotos_get_post_youtube_paginaprincipal(self):
        from .models import Alimentador, Item,Users
        from django.contrib.auth.models import User
        a = Alimentador(alimentadorId="UC300utwSVAYOoRLEqmsprfg", type="youtube")
        a.save()
        i = Item(itemId="HZOodD84MR8")
        i.save()
        response1 = self.client.get('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg/HZOodD84MR8/paginaPrincipal/votopositivo/')
        self.assertEqual(response1.resolver_match.func, views.gestionvotos)
        self.assertEqual(response1.status_code, 302)

    def test_gestionvotos_get_post_flickr_paginaprincipal(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="Madrid", type="flickr")
        a.save()
        i = Item(itemId="49915596093")
        i.save()
        response1 = self.client.get('/MisCosas/flickr/Madrid/49915596093/paginaPrincipal/votopositivo/')
        self.assertEqual(response1.resolver_match.func, views.gestionvotos)
        self.assertEqual(response1.status_code, 302)

    def test_gestionvotos_get_post_lastfm_paginaprincipal(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="Izal", type="lastfm")
        a.save()
        i = Item(itemId="copacabana")
        i.save()
        response1 = self.client.get('/MisCosas/lastfm/Izal/copacabana/paginaPrincipal/votopositivo/')
        self.assertEqual(response1.resolver_match.func, views.gestionvotos)
        self.assertEqual(response1.status_code, 302)

    def test_gestionvotos_get_post_youtube_paginaitem(self):
        from .models import Alimentador, Item, Users
        from django.contrib.auth.models import User
        a = Alimentador(alimentadorId="UC300utwSVAYOoRLEqmsprfg", type="youtube")
        a.save()
        i = Item(itemId="HZOodD84MR8")
        i.save()
        response1 = self.client.get(
            '/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg/HZOodD84MR8/paginaItem/votopositivo/')
        self.assertEqual(response1.resolver_match.func, views.gestionvotos)
        self.assertEqual(response1.status_code, 302)

    def test_gestionvotos_get_post_flickr_paginaitem(self):
        from .models import Alimentador, Item, Users
        from django.contrib.auth.models import User
        a = Alimentador(alimentadorId="Madrid", type="flickr")
        a.save()
        i = Item(itemId="49915596093")
        i.save()
        response1 = self.client.get('/MisCosas/flickr/Madrid/49915596093/paginaItem/votopositivo/')
        self.assertEqual(response1.resolver_match.func, views.gestionvotos)
        self.assertEqual(response1.status_code, 302)

    def test_gestionvotos_get_post_lastfm_paginaitem(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="Izal", type="lastfm")
        a.save()
        i = Item(itemId="copacabana")
        i.save()
        response1 = self.client.get('/MisCosas/lastfm/Izal/copacabana/paginaItem/votopositivo/')
        self.assertEqual(response1.resolver_match.func, views.gestionvotos)
        self.assertEqual(response1.status_code, 302)

    #USERS
    def test_users_get_post(self):
        from .models import Users
        u = Users(username="julian", email="j@j.com", password="julian", image="media/MisCosas/Pérez_Muñoz_Julian_Angel_2-min.jpg")
        u.save()
        response1 = self.client.get('/MisCosas/users/')
        response2 = self.client.post('/MisCosas/users/')
        self.assertEqual(response1.resolver_match.func, views.users)
        self.assertEqual(response2.resolver_match.func, views.users)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    #USER
    def test_user_get_post(self):
        from .models import Users
        u = Users(username="julian", email="j@j.com", password="julian",
                  image="media/MisCosas/Pérez_Muñoz_Julian_Angel_2-min.jpg")
        u.save()
        response1 = self.client.get('/MisCosas/user/julian')
        response2 = self.client.post('/MisCosas/user/julian')
        self.assertEqual(response1.resolver_match.func, views.user)
        self.assertEqual(response2.resolver_match.func, views.user)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    #REGISTER
    def test_register_get(self):
        response1 = self.client.get('/MisCosas/register/')
        self.assertEqual(response1.resolver_match.func, views.register)
        self.assertEqual(response1.status_code, 200)

    #PREGUNTAR
    def test_register_post(self):
        response1 = self.client.post('/MisCosas/register/')
        RegisterForm(data={'Username':'julian',
                                  'Email':'j@j.com',
                                  'Password':'julian',
                                  'image':'media/MisCosas/Pérez_Muñoz_Julian_Angel_2-min.jpg'})
        self.assertEqual(response1.resolver_match.func, views.register)
        self.assertEqual(response1.status_code, 200)

    #LOGIN
    def test_login_get(self):
        response1 = self.client.get('/MisCosas/login/')
        self.assertEqual(response1.resolver_match.func, views.login_view)
        self.assertEqual(response1.status_code, 302)

    def test_login_post(self):
        response1 = self.client.post('/MisCosas/login/')
        LoginForm(data={'Username':'Pedro',
                               'Password': 'julian'})
        self.assertEqual(response1.resolver_match.func, views.login_view)
        self.assertEqual(response1.status_code, 302)

class TestHTML(TestCase):

    def test_index(self):
        checks = ["<h1>Mis Cosas</h1>"]
        response = self.client.get('/MisCosas/')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_register(self):
        checks = ["<h1> Crea tu usuario</h1>"]
        response = self.client.get('/MisCosas/register/')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_user(self):
        from .models import Users
        u = Users(username="julian", email="j@j.com", password="julian",
                  image="media/MisCosas/Pérez_Muñoz_Julian_Angel_2-min.jpg")
        u.save()
        checks = ["<h5>Aquí entontrás los items que has votado en la aplicación</h5>"]
        response = self.client.get('/MisCosas/user/julian')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_users(self):
        checks = ["<h1>Usuarios</h1>"]
        response = self.client.get('/MisCosas/users/')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_alimentadores(self):
        checks = ["<h1>Alimentadores</h1>"]
        response = self.client.get('/MisCosas/alimentadores/')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_alimentador_youtube(self):
        checks = ["<h2 class='youtube'><i class='fab fa-youtube'></i>Youtube</h2>"]
        response = self.client.get('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_alimentador_flickr(self):
        checks = ["<h2 class='flickr'><i class='fab fa-flickr'></i>Flickr</h2>"]
        response = self.client.get('/MisCosas/flickr/Madrid')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_item_youtube(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="UC300utwSVAYOoRLEqmsprfg", type="youtube")
        a.save()
        i = Item(itemId="HZOodD84MR8")
        i.save()
        checks = ["<h3><i class='fab fa-youtube'></i>Youtube</h3>"]
        response = self.client.get('/MisCosas/youtube/UC300utwSVAYOoRLEqmsprfg/HZOodD84MR8')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_item_flickr(self):
        from .models import Alimentador, Item
        a = Alimentador(alimentadorId="Madrid", type="flickr")
        a.save()
        i = Item(itemId="49915596093")
        i.save()
        checks = ["<h3><i class='fab fa-flickr'></i>Flickr</h3>"]
        response = self.client.get('/MisCosas/flickr/Madrid/49915596093')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

class TestForms(TestCase):

    def test_login_form(self):
        form = LoginForm(data={'Username': 'Julian',
                               'Password': 'julian'})
        self.assertTrue(form.is_valid())

    def test_login_form_error(self):
        form = LoginForm(data={'Username': 'Julian',
                               'Password': ''})
        self.assertEquals(len(form.errors), 1)

    def test_register_form(self):
        form = RegisterForm(data={'Username':'julian',
                                  'Email':'j@j.com',
                                  'Password':'julian',
                                  'image': ''})
        self.assertEquals(len(form.errors), 0)

    def test_register_form_error(self):
        form = RegisterForm(data={'Username':'julian',
                                  'Email':'jj',
                                  'Password':'julian',
                                  'image':''})
        self.assertEquals(len(form.errors), 1)

    def test_comentario_form(self):
        form = comentarioForm(data={'comentario': 'julian',
                                  'imagen': ''})
        self.assertEquals(len(form.errors), 0)

    def test_comentario_form_error(self):
        form = comentarioForm(data={'comentario': '',
                                  'imagen': ''})
        self.assertEquals(len(form.errors), 1)


class TestModels(TestCase):

    def test_alimentador(self):
        from .models import Alimentador
        a = Alimentador(alimentadorId="UC300utwSVAYOoRLEqmsprfg", type="youtube")
        a.save()
        self.assertEqual(a.alimentadorId, "UC300utwSVAYOoRLEqmsprfg")
        self.assertEqual(a.type, "youtube")

    def test_item(self):
        from .models import Item
        i = Item(itemId="HZOodD84MR8")
        i.save()
        self.assertEqual(i.itemId, "HZOodD84MR8")

    def test_users(self):
        from .models import Users
        u = Users(username="Julian", email="julian@julian.com")
        u.save()
        self.assertEqual(u.username, "Julian")
        self.assertEqual(u.email, "julian@julian.com")


    def test_votos(self):
        from .models import Users,Item, Voto
        i = Item(itemId="HZOodD84MR8")
        i.save()
        u = Users(username="Julian", email="julian@julian.com")
        u.save()
        v = Voto(usuario=u, item=i, estado="estadopositivo")
        v.save()
        self.assertEqual(v.usuario.username, "Julian")
        self.assertEqual(v.item.itemId, "HZOodD84MR8")
        self.assertEqual(v.estado, "estadopositivo")

    def test_comentario(self):
        from .models import Users,Item, Comentario
        i = Item(itemId="HZOodD84MR8")
        i.save()
        u = Users(username="Julian", email="julian@julian.com")
        u.save()
        c = Comentario(usuario=u, item=i, cuerpo="comentario de test")
        c.save()
        self.assertEqual(c.usuario.username, "Julian")
        self.assertEqual(c.item.itemId, "HZOodD84MR8")
        self.assertEqual(c.cuerpo, "comentario de test")