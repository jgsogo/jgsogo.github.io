---
lang: es
title: RENFE -- Mapa dinámico de circulaciones
date: 2015-08-25
author: jgsogo
category: Projects
tags: 
  - renfe
  - railway
  - geo
  - cartodb
---

Hace unos días me propuse hacer un mapa dinámico con [CartoDB](https://cartodb.com/) en el que se
mostraran los trenes de RENFE moviéndose con la intención de probar la herramienta y experimentar
con sus posibilidades. El caso es que el proyecto crece, los datos no están tan disponibles como
uno quisiera y empiezan a aparecer los famosos *"ya que..."*.

<!--more-->

Durante la recogida de datos para este mapa surgen algunas ideas relacionadas como la construcción
de un grafo con la infraestructura de transporte para realizar análisis que permitan optimizar
costes, tiempos, o estudiar problemas en la infraestructura. Es de imaginar que ADIF dispone de
algo parecido y lo utiliza, así que el objetivo es fundamentalmente exploratorio para empezar a
estudiar sistemas de transporte [^1].

[^1]: Andrew Sherratt, 2005. Portages. http://www.archatlas.org/Portages/Portages.php

Ideas previas
-------------
Como siempre lo primero es buscar un poco por Internet para ver quién ha hecho algo ya y, como siempre,
sin necesidad de bucear demasiado, aparecen algunos buenos resultados:

* <content-twitter-user user="victorianoi">Victoriano</content-twitter-user> tiene un mapa donde muestra
  los [trenes de larga distancia en 2013](https://victoriano-v21.cartodb.com/viz/aac847aa-e882-11e2-bc2b-d90ab36db2dd/public_map) (ver imagen más abajo),
  sin embargo no es exactamente lo que busco. De todos modos, una pena que los datasets sean privados.
   

  <article-image
    src="/img/2015/renfe-stations-victoriano.png"
    alt="Renfe - Trenes de larga distancia 2013"
    caption="Trenes de larga distancia 2013. Los puntos naranjas son la estaciones según el nº de trenes que salen de esa estación.
     El azul es el nº de conexiones posibles con billete único que vende Renfe en viaje directo
     o con transbordo. Autor: Victoriano"></article-image>
    
* Buscando un poco más encontramos los mapas de [Astroide](https://astroide.cartodb.com/maps), otro usuario de CartoDB que nos ofrece unos
  mapas mucho más interesantes para lo que quiero hacer, y que además ofrece públicamente los
  datasets: un mapa dinámico con los [trenes de largo recorrido](https://astroide.cartodb.com/viz/83f346cc-18bc-11e5-a62d-0e9d821ea90d/public_map)
  y otro con los [trenes de mercancias](https://astroide.cartodb.com/viz/5b6b5838-1aa7-11e5-858b-0e018d66dc29/public_map),
  que reproduzco a continuación:
  

  <article-image
    src="/img/2015/renfe-stations-astroide-largadistancia.png"
    alt="Renfe - Trenes de larga distancia"
    caption="Trenes de Larga Distancia. Recorrido efectuado por trenes de Larga Distancia. Estudio del uso de bases de datos NoSQL en
     la Fundación de los Ferrocarriles Españoles. Autor: Astroide"></article-image>

  <article-image
    src="/img/2015/renfe-stations-astroide-mercancias.png"
    alt="Renfe - Trenes de mercancias"
    caption="Trenes de mercancías. Reconstrucción del movimiento de los trenes de mercancías. Estudio del uso de bases de datos NoSQL en
     la Fundación de los Ferrocarriles Españoles. Autor: Astroide"></article-image>
  
  Estos dos mapas son públicos y los datasets pueden descargarse, uno de ellos me será de muchísima
  utilidad: la información con las líneas de la infraestructura, ¿están todas las líneas activas? Por
  si acaso contacto con el usuario para confirmarlo y para saber si puede también proporcionarme los
  datos de las líneas desmanteladas que ya no están operativas.

Los mapas de Astroide muestran básicamente el resultado al que quiero llegar, pero el problema que
me planteo no es tanto obtener el mapa como disfrutar del camino hasta conseguirlo. Además, echo de
menos los trenes de media distancia y regionales, ¡y las estaciones!. Me pregunto: ¿cómo quedará el
mapa si se combinan todos estos trenes en una única visualización y mostramos también las estaciones?


Definición del problema
-----------------------
El reto sigue presente a pesar de los recursos que se han encontrado: para realizar mi mapa dinámico con
las circulaciones de trenes necesito posicionar las estaciones, conseguir los horarios de los trenes y
luego muestrear su posición a lo largo de un día o de una semana para mostrarlos en el mapa.

### La infraestructura: estaciones y líneas

Uno de los primeros pasos que me propongo dar es crear un mapa estático con la infraestructura, básicamente
reproducir la capa de ferrocarriles que supongo que estará disponible en muchos GIS. Para ello necesito:

* los recorridos de las líneas (<nuxt-link to="/blog/2015-08-31-renfe-project-lines">ver artículo</nuxt-link>), y
* la posición de las estaciones (<nuxt-link to="/blog/2015-08-27-renfe-project-stations">ver artículo</nuxt-link>).

En la infraestructura quiero mostrar tanto las líneas que actualmente están en funcionamiento como las
líneas que ya han sido desmanteladas. Asimismo quiero diferenciar por colores según los anchos (FEVE,
métrico, internacional, ibérico) y también identificar qué tramos están electrificados.

En cuanto a las estaciones, el objetivo será mostrar en el mapa la posición de todos los edificios
que hayan ofrecido este servicio. Podrían categorizarse en función de las prestaciones de cada uno
de ellos: accesibilidad, área comercial,...

Una vez que tenga disponibles estos datos visuales, el objetivo será crear un **grafo de la infraestructura
donde los nodos sea estaciones o bifurcaciones y los arcos estén formados por los itinerarios**. Gracias
a este grafo se podrán reconstruir las circulaciones de trenes entre estaciones no contiguas, analizar la
demanda de la infraestructura, las consecuencias de fallos en el servicio, alternativas de recuperación, etc.
No obstante, su construcción resulta compleja, tal y como se mostrará en el artículo correspondiente.

<article-image
    src="/img/2015/jgraph-transport-system.png"
    alt="Visualización de un sistema de transporte sobre el mapa de Europa"
    caption="Visualización como grafo de una red de transporte sobre el mapa de Europa. Fuente: JGraphX User Manual (https://jgraph.github.io/mxgraph/docs/manual_javavis.html)."></article-image>


### Circulaciones de trenes

El otro elemento del mapa son los datos de explotación de la infraestructura: la circulación de los
trenes. Necesito obtener los horarios de todos ellos (estaciones, hora de salida y llegada,...)
para poder identificar en qué lugar se encuentran en cada momento.

RENFE no ofrece esta información de una forma amigable a través de algún tipo de API, tampoco es una
información que haya encontrado en alguna web de la administración como [datos.gob.es](http://datos.gob.es/), así que
habrá que obtenerlos de alguna otra manera (scraping).

Estos datos de los trenes se podrán combinar con los datos del grafo de la infraestructura (y
ayudarán también a construirlo) para generar el mapa dinámico pretendido. Además,
la información disponible de esta manera permitirá realizar diferentes estudios.


Más sobre el proyecto
---------------------
El proyecto se desarrolla en los siguientes artículos:

* Mapa dinámico de circulaciones (<nuxt-link to="/blog/2015-08-25-renfe-project">ver artículo</nuxt-link>).
* Geolocalización de estaciones (ADIF) (<nuxt-link to="/blog/2015-08-27-renfe-project-stations">ver artículo</nuxt-link>).
* La infraestructura ferroviaria (ADIF) (<nuxt-link to="/blog/2015-08-31-renfe-project-lines">ver artículo</nuxt-link>).
* Circulaciones de trenes (RENFE) (<nuxt-link to="/blog/2015-09-01-renfe-project-trains">ver artículo</nuxt-link>).
