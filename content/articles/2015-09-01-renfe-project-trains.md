---
lang: es
title: Circulaciones de trenes (RENFE)
date: 2015-09-01
author: jgsogo
category: Projects
tags: 
  - renfe
  - railway
  - geo
  - cartodb
---

Una fuente de información importantísima para el <nuxt-link to="/blog/2015-08-25-renfe-project">proyecto RENFE</nuxt-link>
son los horarios de los trenes, gracias a
ellos he podido estimar la zona que debe ocupar cada estación (algoritmo de trilateración) identificando
errores de posicionamiento gracias a los tiempos de circulación entre estaciones. Sin embargo, esta
información no es facilitada por RENFE en un formato adecuado sino que hay que extraerla a través de los
formularios de su web. Podéis haceros una idea de la técnica empleada.

<!--more-->

<article-image
    src="/img/2015/renfe-trains-timetable.png"
    alt="Horario del tren MD 18001."
    caption="Horario del tren MD 18001 entre Madrid y Valladolid (Fuente: RENFE http://horarios.renfe.com/HIRRenfeWeb/recorrido.do?O=17000&D=10600&F=01-09-2015&T=18001&G=1&TT=MD&ID=s&FDS=2015-06-14&DT=2%20h.%2052%20min)."></article-image>


De esta forma, a través de la web de RENFE, puedo conocer en qué estaciones hace parada cada tren y los horarios
de llegada y de salida. En total, a lo largo de una semana, he obtenido que se mueven unas 1100
composiciones distintas desde 5500 cabeceras. ¿Muchas? ¿Pocas? Eso lo podremos ver en el mapa dinámico con
los movimientos de los trenes.


Los trenes
----------

### Tipos de trenes

Me ha sorprendido la cantidad de tipos de trenes que aparecen. La lista completa la forman 26 tipos distintos: ``ALSA``,
``ALSINA``, ``ALTARIA``, ``ALVIA``, ``AV City``, ``AVANT``, ``AVE``, ``AVE-TGV``, ``BAILE BUS``, ``BUS ALOSA``,
``CERCANIAS``, ``EUROMED``, ``FRS``, ``INTERCITY``, ``LD-AVE``, ``MD``, ``R. EXPRES``, ``REG ESP``, ``REG EXP``,
``REG. EXP``, ``REG. EXP.``, ``REGIONAL``, ``TALGO``, ``TRENCELTA``, ``TRENHOTEL`` y ``VIA ESTRE``. Se puede observar
que los nombres no están homogeneizados (hay cinco formas de hacer referencia a los Regional Express) y además, me
ha sorprendido mucho ver que RENFE opera algunos autobuses ¡!.

El caso es que tanta fragmentación no es útil, yo he decidido agruparlos en las tipologías clásicas más
próximas al entendimiento común:

* AVE: ``AVE``, ``AVE-TGV``, ``LD-AVE``, ``AV City``.
* Alta Velocidad (no AVE): ``ALTARIA``, ``ALVIA``, ``AVANT``, ``EUROMED``.
* Larga distancia: ``TALGO``, ``TRENHOTEL``
* Media distancia: ``INTERCITY``, ``MD``.
* Regionales: ``R. EXPRES``, ``REG ESP``, ``REG EXP``, ``REG. EXP``, ``REG. EXP.``, ``REGIONAL``.
* Cercanías: ``CERCANIAS``
* Otros trenes: ``TRENCELTA``, ``VIA ESTRE``
* Autobuses: ``ALSA``, ``ALSINA``, ``BAILE BUS``, ``BUS ALOSA``.
* Ferry: ``FRS``

### Horarios de trenes

Una vez obtenida la información de RENFE, he preparado unas clases para acceder a los datos de forma ordenada,
de tal forma que se puedan hacer las consultas por identificador de tren, por parada, día de la semana,...

Gracias a estos horarios también puedo estimar las distancias entre estaciones y ayudar al algoritmo de
posicionamiento de las mismas a detectar errores.

### Trenes compuestos

Un problema que he encontrado y que aún no he resuelto son los trenes que se unen o se separan en ciertas
estaciones, ocurre a menudo con los de alta velocidad que suben a Galicia. La dificultad radica en que estos
trenes tienen el mismo identificador durante todo su recorrido para ambas ramas.

Otra cosa más de trabajo pendiente :/



Más sobre el proyecto
---------------------
El proyecto se desarrolla en los siguientes artículos:

* Mapa dinámico de circulaciones (<nuxt-link to="/blog/2015-08-25-renfe-project">ver artículo</nuxt-link>).
* Geolocalización de estaciones (ADIF) (<nuxt-link to="/blog/2015-08-27-renfe-project-stations">ver artículo</nuxt-link>).
* La infraestructura ferroviaria (ADIF) (<nuxt-link to="/blog/2015-08-31-renfe-project-lines">ver artículo</nuxt-link>).
* Circulaciones de trenes (RENFE) (<nuxt-link to="/blog/2015-09-01-renfe-project-trains">ver artículo</nuxt-link>).
