Trilateración con error
=======================

:date: 2015-08-25 18:34
:tags: optimization, multivariate,
:slug: trilateration-with-error
:status: draft
:template2: draft.html

.. DANGER::
   Este artículo está en construcción... ¿`quieres colaborar <https://github.com/jgsogo/jgsogo.github.io>`__?


.. contents::

Durante la realización del `proyecto RENFE`_ tuve que `geolocalizar algunas estaciones`_ utilizando información
inderecta obtenida a través de los horarios de circulación de los trenes. El objetivo era calcular la zona
donde la probabilidad de encontrar una estación era máxima según las distancias recorridas por los trenes que
paran en ella desde otras estaciones cuya posición si era conocida.

.. _proyecto RENFE: {filename}/Projects/renfe_project.rst
.. _geolocalizar algunas estaciones: {filename}/Projects/renfe_project_stations.rst#trilateracion

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

.. code-block:: python

   [
    {'latitude': x.xxx, 'longitude': x.xxxx, 'meters': [x.xx, xx.xx, ...]},
    {'latitude': x.xxx, 'longitude': x.xxxx, 'meters': [x.xx, xx.xx, ...]},
    ...
   ]

es decir, datos de latitud y longitud acompañados de distancias en metros hasta la estación objetivo. En
un mundo ideal todas esas medidas de distancia deberían ser la misma, pero la realidad no es tan
benigna.

Distancias: Distribución de probabilidad
++++++++++++++++++++++++++++++++++++++++
El primer paso que realizo es calcular la distribución de probabilidad normal que sirve para estas
distancias.
