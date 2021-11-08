---
lang: es
title: Trilateración con error
date: 2015-08-25
author: jgsogo
category: Algorithms
tags: 
  - optimization
  - multivariate
draft: true
---

Durante la realización del <nuxt-link to="/blog/2015-08-25-renfe-project">proyecto RENFE</nuxt-link>
tuve que <nuxt-link to="/blog/2015-08-27-renfe-project-stations">geolocalizar algunas estaciones</nuxt-link> utilizando información
inderecta obtenida a través de los horarios de circulación de los trenes. El objetivo era calcular la zona
donde la probabilidad de encontrar una estación era máxima según las distancias recorridas por los trenes que
paran en ella desde otras estaciones cuya posición si era conocida.

<!--more-->

Las fuentes de error eran diversas:

* La posición de las estaciones conocidas: a pesar de que las coordenadas GPS son un dato exacto, éste puede
  no corresponderse con el punto donde el tren efectúa la parada.
* La velocidad de los trenes entre las estaciones: conocemos las prestaciones del tren (velocidad máxima), pero
  no el perfil de velocidades de la línea ni las curvas de aceleración y frenada.
* La distancia real recorrida: las distancias las estimamos en línea recta, sin considerar las curvas de la
  infraestructura real.

Plantear el problema como trilateración con error parece una opción interesante que además quería explorar.


Los datos
---------
La entrada de cada problema consistía, por tanto, en un vector de características como el siguiente:

```python
[
    {'latitude': x.xxx, 'longitude': x.xxxx, 'meters': [x.xx, xx.xx, ...]},
    {'latitude': x.xxx, 'longitude': x.xxxx, 'meters': [x.xx, xx.xx, ...]},
    ...
]
```

es decir, datos de latitud y longitud acompañados de distancias en metros hasta la estación objetivo. En
un mundo ideal todas esas medidas de distancia deberían ser la misma, pero la realidad no es tan
benigna.

### Distancias: Distribución de probabilidad

El primer paso que realizo es calcular la distribución de probabilidad normal que sirve para estas
distancias.
