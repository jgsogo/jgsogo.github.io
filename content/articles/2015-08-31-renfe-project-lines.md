---
lang: es
title: La infraestructura ferroviaria (ADIF)
date: 2015-08-31
author: jgsogo
category: Projects
tags: 
  - renfe
  - railway
  - geo
  - cartodb
---

El primer paso del <nuxt-link to="/blog/2015-08-25-renfe-project">proyecto RENFE</nuxt-link> consistió en
<nuxt-link to="/blog/2015-08-27-renfe-project-stations">posicionar las estaciones</nuxt-link>. Una vez realizada esta tarea
puedo construir un mapa con los recorridos de los trenes utilizando la información de horarios y paradas que
aparece en la web de RENFE. De esta forma puedo construir el trayecto seguido por un tren cualquiera, por un
tipo de trenes o por todos ellos y, lo que es más importante, puedo saber qué estaciones están conectadas
con cuales, lo que me permitirá construir **el grafo de la infraestructura**.

<!--more-->

<article-image
    src="/img/2015/renfe-lines-alvia-with-errors.png"
    alt="Mapa de conexiones de los trenes ALVIA de RENFE"
    caption="Grafo de conexiones de los trenes ALVIA de RENFE, se muestra con colores el número de composiciones
   que hacen uso de cada conexión."></article-image>


Detección de errores
--------------------
En el gráfico anterior se puede ver un dibujo esquemático de las conexiones que cubren los trenes ALVIA,
en él se aprecian dos errores claros de posicionamiento de las estaciones. Uno de ellos está en el trayecto
entre Córdoba y Málaga donde se realizan paradas en Puente Genil (correctamente situado en el mapa)
y Antequera (que aparece erroneamente en Valencia); el otro está relacionado con una estación gallega
que aparece en tierras cántabras.

Podemos detectar estos errores de dos formas:

* Visualmente: en el caso anterior está claro que Antequera es un error de posicionamiento.
* Con un algoritmo: puesto que tengo los horarios de los trenes puedo calcular la velocidad a la
  cual deberían viajar para recorrer la distancia entre cada par de estaciones, si esta velocidad
  está fuera de unos rangos normales sabré que alguna de las estaciones (origen o destino) está
  mal posicionada, ejecutando el algoritmo para todos los pares de estaciones puedo resolver la ambigüedades.

Una vez que he detectado las estaciones mal posicionadas puedo utilizar el
<nuxt-link to="/blog/2015-08-25-trilateration-with-errors">algoritmo de trilateración</nuxt-link>
para calcular su posición correcta o bien solucionar el problema manualmente.

Con los datos corregidos ya puedo generar mapas con las conexiones directas entre estaciones
según el tipo de tren como es el caso de la siguiente figura donde aparecen las conexiones
de trenes MD, TALGO y Tren Hotel.

<article-image
    src="/img/2015/renfe-lines-md-talgo-trenhotel.png"
    alt="Mapa de conexiones de los trenes MD, TALGO y Tren Hotel"
    caption="Mapa de conexiones de los trenes MD (naranja), TALGO (rojo) y Tren Hotel (verde) de RENFE; en blanco se
   muestran las estaciones donde hacen parada."></article-image>


Grafo de líneas
---------------
El objetivo que persigo en esta parte es construir un grafo con toda la infraestructura ferroviaria
española, donde los nodos sean las estaciones y las uniones entre líneas y los arcos sean las vías
que los conectan. Idealmente cada arco y nodo podrá tener sus atributos indicando si está electrificado,
cuál es la velocidad máxima, ancho de vía, distancia,...

Para lograr realizar este grafo me tengo que apoyar en los grafos por tipo de tren del apartado anterior
para saber qué estaciones están conectadas con cuáles, pero la dificultad estriba en relacionar esas
estaciones con la infraestructura subyacente.

Como indiqué en el artículo de introducción, gracias a [Astroide](https://astroide.cartodb.com/maps) he conseguido la información de las
líneas, pero no se incluyen las estaciones ni las uniones entre líneas.


### Posición de las estaciones sobre las líneas

Una vez que he realizado el trabajo de posicionamiento de las estaciones en el mapa puedo proyectarlas
sobre la línea más cercana, son unos cálculos triviales utilizando la librería [shapely](http://toblerity.org/shapely/manual.html). Esta proyección
que ya hicimos en el artículo sobre (<nuxt-link to="/blog/2015-08-27-renfe-project-stations">estaciones</nuxt-link>) nos
sirve también para validar el posicionamiento de las mismas.

Sería muy interesante contar con las líneas de Portugal (algunas estaciones pertenecen a este país) y
con la información de vías desmanteladas para validar la posición de estaciones en desuso.

### Cruces entre líneas

El otro algoritmo que he aplicado sobre las líneas es el cálculo de las intersecciones que se producen
entre ellas buscando puntos comunes. Este algoritmo identifica tres tipos de puntos comunes:

* las intersecciones entre líneas: lugares donde una línea pasa sobre otra sin que haya unión entre ambas.
* los puntos de unión: lugares donde dos vías se unen para formar una sola (o separan).
* los empalmes: lugares donde empieza una vía a continuación de otra.

<article-image
    src="/img/2015/renfe-lines-leon.png"
    alt="Intersecciones entre líneas en las proximidades de León."
    caption="Mapa de intersecciones entre líneas (puntos blancos) en las proximidades de la ciudad de León."></article-image>

Sin embargo la casuística es muy grande y hay muchos errores en los que aún tengo que trabajar:

* **Falsos positivos**: los cruces entre líneas sin unión entre ellas no deben ser incluídos en el grafo resultante.
* **Falsos negativos**: uniones entre líneas que no comparten ningún punto geométrico común por redondeos u
  errores en los datos. El algoritmo debe permitir cierto error a la hora de identificar los cruces (sin
  introducir más falsos positivos).

<base-alert type="next">
El resultado con el grafo final tendrá que esperar un poco más, aún está en construcción.
</base-alert>

Más sobre el proyecto
---------------------
El proyecto se desarrolla en los siguientes artículos:

* Mapa dinámico de circulaciones (<nuxt-link to="/blog/2015-08-25-renfe-project">ver artículo</nuxt-link>).
* Geolocalización de estaciones (ADIF) (<nuxt-link to="/blog/2015-08-27-renfe-project-stations">ver artículo</nuxt-link>).
* La infraestructura ferroviaria (ADIF) (<nuxt-link to="/blog/2015-08-31-renfe-project-lines">ver artículo</nuxt-link>).
* Circulaciones de trenes (RENFE) (<nuxt-link to="/blog/2015-09-01-renfe-project-trains">ver artículo</nuxt-link>).
