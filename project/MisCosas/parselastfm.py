#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

class LastfmHandler(ContentHandler):

    def __init__(self):
        self.inEntry = False
        self.inContent = False
        self.imagenbuena  = False
        self.content = ""
        self.alimentador = ""
        self.tituloAlimentador = ""
        self.enlaceAlimentador = ""
        self.alimentadorId = ""
        self.tituloItem = ""
        self.enlaceItem = ""
        self.itemId = ""
        self.fotoItem = ""

    def startElement(self, name, attrs):
        if name == 'artist':
            self.inEntry = True
        elif self.inEntry:
            if name == 'name':
                self.inContent = True
            if name == 'url':
                self.inContent = True

        elif self.inEntry == False:
            if name == 'name':
                self.inContent = True
            elif name == 'url':
                self.inContent = True
            elif name == 'image' and attrs.get('size') == 'extralarge' :
                self.inContent = True
                self.imagenbuena = True


    def endElement(self, name):
        if name == 'artist':
            self.inEntry = False

        elif self.inEntry:
            if name == 'name':
                self.tituloAlimentador = self.content
                self.content = ""
                self.inContent = False

            if name == 'url':
                self.enlaceAlimentador = self.content
                self.content = ""
                self.inContent = False

        elif self.inEntry == False:

            if name == 'name':
                self.tituloItem = self.content
                self.content = ""
                self.inContent = False

            elif name == 'url':
                self.enlaceItem = self.content
                self.content = ""
                self.inContent = False

            elif name == 'image':
                if self.imagenbuena:
                    self.fotoItem = self.content
                    self.content = ""
                    self.inContent = False
                    self.imagenbuena = False

                    from .models import Item, Alimentador
                    if self.alimentador == "":
                        try:
                            a = Alimentador.objects.get(alimentadorId=self.tituloAlimentador, nombre=self.tituloAlimentador,
                                                        enlace=self.enlaceAlimentador, type="lastfm")
                        except Alimentador.DoesNotExist:
                            a = Alimentador(alimentadorId=self.tituloAlimentador, nombre=self.tituloAlimentador,
                                            enlace=self.enlaceAlimentador, type="lastfm")
                            a.save()

                        self.alimentador = a

                    try:
                        i = Item.objects.get(nombre=self.tituloItem, enlace=self.enlaceItem, itemId=self.tituloItem,
                                             fotoItem=self.fotoItem, alimentador=self.alimentador)
                    except Item.DoesNotExist:
                        newItem = Item(nombre=self.tituloItem, enlace=self.enlaceItem, itemId=self.tituloItem,
                                       fotoItem=self.fotoItem, alimentador=self.alimentador)
                        newItem.save()

    def characters(self, chars):
        if self.inContent:
            self.content = self.content + chars
