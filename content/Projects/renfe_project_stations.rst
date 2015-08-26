Geolocalización de estaciones (ADIF)
====================================

:date: 2015-08-25 18:34
:tags: renfe, railway, geo, cartodb
:slug: renfe-project-geo-stations

.. contents::

Dentro del `proyecto RENFE`_ una de las partes más importantes es determinar la posición de las
estaciones en el mapa (latitud y longitud). Una vez más hemos de reunir información de diversas
fuentes y hacerla coherente para generar el *dataset* que necesitamos, en concreto vamos a
combinar datos de las siguientes fuentes:

* Renfe_: en su web podemos consultar un listado de estaciones.
* ADIF_: en la sección "infraestructuras y estaciones" se puede obtener las coordenadas GPS
  de algunas estaciones.
* `La Estación de Tren`_: ofrece un listado de estaciones con sus coordenadas GPS etiquetadas manualmente.

Una vez obtenida la información de estas fuentes tengo que utilizar algunos **algoritmos** para
relacionarlos, hacerlos coherentes y completarlos. Y por supuesto, un poquito de ayuda manual
nunca les va a venir mal.

.. _proyecto RENFE: {filename}/Projects/renfe_project.rst
.. _Renfe: http://www.renfe.com/
.. _ADIF: http://adif.es
.. _La Estación de Tren: http://www.laestaciondetren.net/


Listado de estaciones
---------------------
La primera tarea que hay que realizar es obtener la lista (lo más completa posible) de estaciones. En
la web de Renfe tenemos un link [#]_, de donde podemos obtener con un simple *script* un primer listado.

.. [#] RENFE. Listado de estaciones. URL: https://venta.renfe.com/vol/estacionesAccesibleVXY.do

Cada estación tiene un nombre y un identificador. Este identificador es único y está formado por 5 dígitos,
sin embargo, en algunos casos se incorporan letras cuando no identifica una estación concreta sino una ciudad
que dispone de varias estaciones: :code:`MADRI` para Madrid, :code:`IRUN-` para Irún-Hendaya,... en cualquier
caso, cada estación de la ciudad posee un identificador numérico único.

Los identificadores numéricos, donde aparecen, son la primera opción para identificar las estaciones; sin
embargo, en muchos otros casos, tendremos que utilizar los nombres y comparar de forma inexacta cadenas de
texto para identificar la estación (ver `comparación inexacta de cadenas <{filename}/Algorithms/fuzzy-string-comparison.md>`__). Estos nombres alternativos
los guardaremos como *alias* de la estación para utilizarlos en búsquedas futuras.


Posicionamiento
---------------
Una vez obtenido el listado de estaciones tengo que georreferenciarlas sobre el mapa. Como he indicado
más arriba, para esta tarea utilizo varias fuentes:

ADIF
++++
En la web de ADIF se pueden consultar los datos GPS de algunas estaciones, extraerlos del HTML no es
complicado, tal y como se puede ver en la imagen siguiente:

.. figure:: {filename}/images/renfe-stations-adif-gps.png
   :align: center
   :alt: Coordenadas GPS de una estación en la web de ADIF

   Coordenadas GPS de una estación en la web de ADIF.

Sin embargo, las URLs de esta página siguen un patrón que no he podido identificar, aparece un identificador
numérico al final que impide construirlas de forma automática. Algunos ejemplos:

===== ============= =====
 ID    Nombre        URL
===== ============= =====
23004 Pontevedra    http://www.adif.es/es_ES/infraestructuras/estaciones/23004/informacion_000047.shtml
30002 Plasencia     http://www.adif.es/es_ES/infraestructuras/estaciones/30002/informacion_000141.shtml
74200 Huesca        http://www.adif.es/es_ES/infraestructuras/estaciones/74200/informacion_000099.shtml
===== ============= =====

Como consecuencia de ese parámetro debemos utilizar alguna otra técnica para acceder a las páginas de
detalle de cada una de las estaciones: se puede utilizar un script que trabaje con el mapa o partir de
la pestaña de "Llegadas y Salidas" a la que se puede acceder utilizando únicamente el identificador de
la estación (ej.: :code:`http://www.adif.es/AdifWeb/estacion_mostrar.jsp?e=20213`). Una vez ahí se puede
parsear la web para obtener el link de la pestaña "Información" donde tenemos las coordenadas GPS.

Podría parecer que aquí termina el trabajo, pero no es así; en la web de ADIF aparecen algo más de
200 estaciones, pero tenemos que geoposicionar unas 1200.

La Estación de Tren
+++++++++++++++++++
**Fernando Solabre** es el autor de la web La Estación de Tren, en la que se muestra un listado de 1915 estaciones
geolocalizadas manualmente e identificadas por el nombre que aparece en los mapas. El trabajo realizado merece
una mención especial y me va a permitir posicionar muchas estaciones.

Para utilizar este dataset nos enfrentamos a dos dificultades: identificar la estación y convertir las coordenadas
de UTM a longitud/latitud. Para la primera de ellas utilizaremos la comparación inexacta de cadenas a la que
hemos hecho mención anteriormente, para la segunda utlizamos la librería de Python llamada utm_.

.. _utm: https://github.com/Turbo87/utm

Al automatizar el procesamiento de este conjunto de datos no tengo garantías de que la identificación de
las estaciones haya sido correcta, confío en que los algoritmos posteriores muestren incongruencias ante
un dato erroneo y me permita identificarlos.

Buscadores/Mapas
++++++++++++++++
Una tercera vía que he utilizado para geoposicionar las estaciones ha sido utlizar los servicios de
Internet que permiten obtener las coordenadas de un punto a partir de su dirección. Hay una
fantástica librería que nos permite hacerlo sin despeinarnos: geopy_.

.. _geopy: https://github.com/geopy/geopy

Como dato de entrada para todos estos servicios he utilizado el nombre de la estación con lo cual la
fiabilidad de los resultados es bastante baja en ocasiones (se obtienen estaciones dispersas
por toda la Tierra).

Puesto que dispongo de varias respuestas para cada estación puedo combinarlas para intentar mejorar
el resultado. Así filtro los *outliers* utilizando un test conocido como *median-absolute-deviation* (MAD_)
y posteriormente me quedo con la posición correspondiente a la media aritmética de todas las respuestas.

.. _MAD: https://stackoverflow.com/questions/22354094/pythonic-way-of-detecting-outliers-in-one-dimensional-observation-data/22357811#22357811

Estaciones sin datos
--------------------

Trilateración
+++++++++++++


Proyección sobre las líneas
---------------------------
