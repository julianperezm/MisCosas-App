#!/usr/bin/python3

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

class YTHandler(ContentHandler):

    def __init__(self):
        self.inEntry = False  # Para saber si estamos dentro de entry
        self.inContent = False  # Si tenemos contenido que queremos leer
        self.inMediaGroup = False
        self.inAuthor = False
        self.content = ""
        self.title = ""
        self.link = ""
        self.videoId = ""
        self.fotoVideo = ""
        self.nombreCanal = ""
        self.enlaceCanal = ""
        self.fecha = ""
        self.descripcion = ""
        self.alimentador = ""
        self.alimentadorId = ""
        self.nombreAcortado = ""

    def startElement(self, name, attrs):
        if name == 'entry':
            self.inEntry = True

        elif self.inEntry:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')
            elif name == 'yt:videoId':
                self.inContent = True
            elif name == 'media:group':
                self.inMediaGroup = True
            elif name == 'author':
                self.inAuthor = True
            elif name == 'published':
                self.inContent = True
            elif name == 'yt:channelId':
                self.inContent = True
        if self.inMediaGroup:
            if name == 'media:thumbnail':
                self.fotoVideo = attrs.get('url')
            if name ==  'media:description':
                self.inContent = True
        if self.inAuthor:
            if name == 'name':
                self.inContent = True
            elif name == 'uri':
                self.inContent = True

    def endElement(self, name):
        if name == 'entry':
            from .models import Item, Alimentador
            self.inEntry = False

            if self.alimentador == "":
                try:
                    a = Alimentador.objects.get(alimentadorId= self.alimentadorId, nombre=self.nombreCanal, enlace=self.enlaceCanal, type="youtube")

                except Alimentador.DoesNotExist:
                    a = Alimentador(alimentadorId= self.alimentadorId, nombre=self.nombreCanal, enlace=self.enlaceCanal, type="youtube")
                    a.save()

                self.alimentador = a

            try:
                i = Item.objects.get(nombre=self.title, enlace=self.link, itemId=self.videoId,
                                            fotoItem=self.fotoVideo, descripcion=self.descripcion,
                                            alimentador=self.alimentador)
            except Item.DoesNotExist:
                newItem = Item(nombre=self.title, enlace=self.link, itemId=self.videoId,
                                            fotoItem=self.fotoVideo, descripcion=self.descripcion,
                                            alimentador=self.alimentador)
                newItem.save()

        elif name == 'media:group':
            self.inMediaGroup = False

        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False
            elif name == 'yt:videoId':
                self.videoId = self.content
                self.content = ""
                self.inContent = False
            elif name == 'name':
                self.nombreCanal = self.content
                self.content = ""
                self.inContent = False
            elif name == 'uri':
                self.enlaceCanal = self.content
                self.content = ""
                self.inContent = False
            elif name == 'published':
                self.fecha = self.content
                self.content = ""
                self.inContent = False
            elif name == 'media:description':
                self.descripcion = self.content
                self.content = ""
                self.inContent = False
            elif name == 'yt:channelId':
                self.alimentadorId = self.content
                self.content = ""
                self.inContent = False

    def characters(self, chars):
        if self.inContent:
            self.content = self.content + chars
