---
lang: es
title: Mapa dinámico con los trenes (continuará...)
date: 2015-09-22
author: jgsogo
category: Projects
tags: 
  - renfe
  - railway
  - geo
  - cartodb
---

El <nuxt-link to="/blog/2015-08-25-renfe-project">proyecto RENFE</nuxt-link> empieza a dar sus
frutos a pesar de que no puedo dedicarle todo el tiempo que
quisiera (y que probablemente se merezca), así que en un pequeño paréntesis os voy a contar los
avances: ya saco los horarios de todos los trenes, he logrado posicionar la mayoría de las estaciones
(aunque aún me quedan más de 2000 alias por identificar) y ahora también sitúo los trenes dentro
de su trayecto entre estaciones, es decir, que calculo su posición para cualquier instante temporal.

<!--more-->

Y aquí tenéis el resultado. A mí me hipnotiza, y me encanta ver dónde se cruzan los trenes ;D

<iframe width="100%" height="520" frameborder="0" src="https://jgsogo.cartodb.com/viz/1f707e86-613c-11e5-a7e5-0e9d821ea90d/embed_map" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe>

No obstante todavía me queda trabajo por delante, dos *issues* principales:

* No están incluídos los trenes que tienes varias cabeceras o destinos como es el caso de varios que
  con origen o destino en Galicia, por lo que esa parte del mapa está infrarrepresentada.

* Los trenes viajan en línea recta entre las estaciones.

Es segundo punto es un problema relativamente complejo. Gracias a <content-twitter-user user="jgcasta"></content-twitter-user>
tengo las principales líneas
de ferrocarril de España, pero estas líneas no están etiquetadas ni conectadas, son sólo dibujos, líneas.
Lo que me propongo es construir un grafo donde los nodos sean las estaciones y estas líneas los arcos que
las unen de tal manera que cuando un tren vaya de una estación a otra yo sepa sin ambigüedad cuál de los
arcos está siguiendo y pueda proyectar su movimiento sobre él.

Sin embargo, las líneas se cruzan de vez en cuando (sin existir aguja) y otras que deberían estar unidas
están ligeramente separadas con lo que no es fácil identificar qué línea va a continuación de cual otra,
algunos de estos casos se pueden ver en la siguiente figura:

<article-image
    src="/img/2015/renfe-lines-leon.png"
    alt="Intersecciones entre líneas en las proximidades de León."
    caption="Mapa de intersecciones entre líneas (puntos blancos) en las proximidades de la ciudad de León."></article-image>

Me temo que construir este grafo va a requerir bastante trabajo... os mantendré informados.
