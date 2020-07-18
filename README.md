 # Entrega practica
## Datos
* Nombre Julián Ángel Pérez Muñoz
* Titulación: Ingeniería en Tecnologías de la Telecomunicación
* Usuario: Julian
* Video básico (url):https://www.youtube.com/watch?v=IrNbuUpfKVc
* Video parte opcional (url): https://www.youtube.com/watch?v=r1iEacwmG1M
* Despliegue (url): http://julianperezm.pythonanywhere.com/MisCosas/
## Cuenta Admin Site 
* Administrador/finalsat
## Cuentas usuarios
* Julián/julian
* Lucía/lucia 
* Pedro/pedro
## Resumen parte obligatoria
* Voy a comentar algunas peculiaridades de mi práctica que no venían en la guía pero he visto
interesante su implementación:
    * Tratamiento de acentos mediante el uso de la librería "unidecode"
    * Tratamiento de espacios tanto en el alimentador last.fm como en flickr
    * Uso de la clave API en el alimentador last.fm, no lo he subido por privacidad, pero 
    la manera de conseguirlo en este caso es, accediendo a la página https://www.last.fm/api/account/create
    creandonos la cuenta y rellenando los datos que nos piden. El siguiente paso será crear un fichero
    dentro de 'MisCosas' llamado apikeys.py e incluyendo dentro de este la clave en el siguiente formato
    LASTFM_APIKEY = "La clave"
    * He añadido más elementos a la barra de navegación cuando nos encontramos en la página principal para 
    que sea mas facil navegar sobre ella.
    * He separados los alimentadores según de donde sean, youtube, last.fm o flickr.
    * He utilizado el paquete serializers para la creación de las páginas JSON. Al principio habia hecho las páginas de manera
    manual como las XML pero al realizar una comprobacion con parser JSON de python me daba fallo en las ultimas comas de cada
   final de elementos, ya que lo hacia mediante bucles.
## Lista partes opcionales
* Inclusión favicon del sitio
* Visualización de cualquier página en formato JSON y XML
* Incorporación de un alimentador no obligatorio con api key (last.fm)
* Utilización de Bootstrap v4.4
* Inclusión de imagenes en los comentarios a parte del texto.
* Test de views, models, html y forms, incluyendo condiciones de error.
* He utilizado el kit de font awesome para asi poder utilizar iconos como por ejemplo
    los simbolos de los alimentadores o el icono cuando el usuario no tiene foto.
* En los comentarios a parte de el nombre he añadido la foto de usuario.
* Creación página de registro, comprobando si el usuario ya existe y si es así mostrandoselo en pantalla.
* He creado una página de error para en el caso de recursos no encontrados (DEDUG=False).

