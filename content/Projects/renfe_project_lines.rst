La infraestructura ferroviaria (ADIF)
=====================================

:date: 2015-08-25 18:34
:tags: renfe, railway, geo, cartodb
:slug: renfe-project-lines
:status: draft

.. contents::

El primer paso del `proyecto RENFE`_ consistió en
`posicionar las estaciones <{filename}/Projects/renfe_project_stations.rst>`__. Una vez realizada esta tarea
puedo construir un mapa con los recorridos de los trenes utilizando la información de horarios y paradas que
aparece en la web de RENFE. De esta forma puedo construir el trayecto seguido por un tren cualquiera, por un
tipo de trenes o por todos ellos y, lo que es más importante, puede saber qué estaciones están conectadas
con cuales, lo que me permitirá construir **el grafo de la infraestructura**.

.. _proyecto RENFE: {filename}/Projects/renfe_project.rst

.. figure:: {filename}/images/renfe-lines-alvia-with-errors.png
   :align: center
   :alt: Mapa de conexiones de los trenes ALVIA de RENFE

   Grafo de conexiones de los trenes ALVIA de RENFE, se muestra con colores el número de composiciones
   que hacen uso de cada conexión.


Detección de errores
--------------------
En el gráfico anterior se puede ver un dibujo esquemático de las conexiones que cubren los trenes ALVIA,
en él se aprecian dos errores claros de posicionamiento de las estaciones. Uno de ellos está en el trayecto
entre Córdoba y Málaga donde se realizan paradas en Puente Genil (correctamente situado en el mapa)
y Antequera (que aparece erroneamente en Valencia).

Podemos detectar estos errores de dos formas:

* Visualmente: en el caso anterior está claro que Antequera es un error de posicionamiento.
* Con un algoritmo: puesto que tengo los horarios de los trenes puedo calcular la velocidad a la
  cual deberían viajar para recorrer la distancia entre cada par de estaciones, si esta velocidad
  está fuera de unos rangos normales sabré que alguna de las estaciones (origen o destino) está
  mal posicionada, ejecutando el algoritmo entre cada par de estaciones puedo resolver la ambigüedad.

Una vez que he detectado las estaciones mal posicionadas puedo utilizar el algoritmo de trilateración
para calcular su posición correcta o bien solucionar el problema manualmente.


Más sobre el proyecto
---------------------
El proyecto se desarrolla en los siguientes artículos:

* Mapa dinámico de circulaciones (`ver artículo <{filename}/Projects/renfe_project.rst>`__).
* Geolocalización de estaciones (ADIF) (`ver artículo <{filename}/Projects/renfe_project_stations.rst>`__).
* La infraestructura ferroviaria (ADIF)
* Circulaciones de trenes (RENFE) (`ver artículo <{filename}/Projects/renfe_project_trains.rst>`__).