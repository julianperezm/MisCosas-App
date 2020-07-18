#!/usr/bin/python3

from xml.sax.handler import ContentHandler

class FlickrHandler(ContentHandler):

    def __init__(self):
        self.inEntry = False  # Para saber si estamos dentro de entry
        self.inContent = False  # Si tenemos contenido que queremos leer
        self.content = ""
        self.alimentador= ""
        self.tituloAlimentador = ""
        self.enlaceAlimentador = ""
        self.alimentadorId = ""
        self.tituloItem = ""
        self.enlaceItem =""
        self.itemId = ""
        self.fotoItem = ""

    def startElement(self, name, attrs):
        if name == 'entry':
            self.inEntry = True

        elif self.inEntry:
            if name == 'title':
                self.inContent = True
            if name == 'link':
                a = attrs.get('rel')
                if a == 'alternate':
                    self.enlaceItem = attrs.get('href')
                elif a == 'enclosure':
                    self.fotoItem = attrs.get('href')
            if name == 'id':
                self.inContent = True

        elif self.inEntry == False:
            if name == 'link':
                a = attrs.get('rel')
                if a == 'self':
                    self.tituloAlimentador = attrs.get('href')
                    self.tituloAlimentador = self.tituloAlimentador.split('=')[-1]
                    self.tituloAlimentador = self.tituloAlimentador.replace("%20", " ")
                if a == 'alternate':
                    self.enlaceAlimentador = attrs.get('href')
            if name == 'id':
                self.inContent = True

    def endElement(self, name):
        if name == 'entry':
            from .models import Item, Alimentador
            self.inEntry = False

            if self.alimentador == "":
                try:
                    a = Alimentador.objects.get(alimentadorId=self.alimentadorId)
                except Alimentador.DoesNotExist:
                    a = Alimentador(alimentadorId=self.alimentadorId, nombre=self.tituloAlimentador,
                                    enlace=self.enlaceAlimentador, type="flickr")
                    a.save()

                self.alimentador = a

            try:
                i = Item.objects.get(nombre=self.tituloItem, enlace=self.enlaceItem, itemId=self.itemId,
                                     fotoItem=self.fotoItem, alimentador=self.alimentador)
            except Item.DoesNotExist:
                newItem = Item(nombre=self.tituloItem, enlace=self.enlaceItem, itemId=self.itemId,
                               fotoItem=self.fotoItem, alimentador=self.alimentador)
                newItem.save()

        elif self.inEntry:
            if name == 'title':
                self.tituloItem =  self.content
                self.content = ""
                self.inContent = False

            if name == 'id':
                self.itemId = self.content
                self.itemId = self.itemId.split("/")[-1]
                self.content = ""
                self.inContent = False

        elif self.inEntry == False:
            if name == 'id':
                self.alimentadorId = self.content
                self.alimentadorId = self.alimentadorId.split("/")[-1]
                self.content = ""
                self.inContent = False

    def characters(self, chars):
        if self.inContent:
            self.content = self.content + chars
