Webassembly, OpenGL y Qt - Un cubo interactivo en la web
========================================================

:date: 2021-01-19 10:30
:tags: c++, wasm, qt, web
:slug: emscripten-cube

.. contents::

Hace mucho tiempo publiqué un tweet que tuvo cierta tracción, en él mostraba
un cubo interactivo en el navegador que había hecho con C++. La magia detrás
de ese cubo era una aplicación de Qt compilada para Webassembly utilizando un
visor de OpenGL.

.. raw:: html

    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Here it is, a little <a href="https://twitter.com/conan_io?ref_src=twsrc%5Etfw">@conan_io</a>/<a href="https://twitter.com/jfrog?ref_src=twsrc%5Etfw">@jfrog</a>/<a href="https://twitter.com/isocpp?ref_src=twsrc%5Etfw">@isocpp</a> cube running in Chrome compiled to <a href="https://twitter.com/hashtag/webassembly?src=hash&amp;ref_src=twsrc%5Etfw">#webassembly</a> using <a href="https://twitter.com/hashtag/Qt?src=hash&amp;ref_src=twsrc%5Etfw">#Qt</a> 🤠. Just a couple of steps thanks to the packages and recipes provided by <a href="https://twitter.com/bincrafters?ref_src=twsrc%5Etfw">@bincrafters</a> 🤟 I&#39;ll write a making of, promise. <a href="https://t.co/0XPbifrant">pic.twitter.com/0XPbifrant</a></p>&mdash; jgsogo (@jgsogo) <a href="https://twitter.com/jgsogo/status/1089562018355527680?ref_src=twsrc%5Etfw">January 27, 2019</a></blockquote> 
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

En aquel momento dije que documentaría el proceso, pero no lo hice. Hoy, casualidades
del destino, me siento en deuda con esto de nuevo y ha llegado el momento de comentar
cómo se hizo... aunque haya que hacerlo de nuevo porque perdí el código fuente 😅.

He conseguido reproducir el proyecto de una manera más ordenada y quizá algunas de las
cosas que se utlizan aquí podrían incorporarse a los paquetes correspondientes de 
`ConanCenter`_, aunque ése no es el objetivo de este post ni condición para publicarlo.

.. _ConanCenter: https://conan.io/center

Las tecnologías que he utilizado, como ya avanzaba, han sido el conocido framework `Qt`_
y `Emscripten`_ para compilar el código a Webassembly. Con Qt es muy sencillo hacer una 
aplicación de escritorio con un canvas de OpenGL en el que mostrar un cubo, con Emscripten
resulta trivial compilar un proyecto para Webassembly y utilizar el navegador para
renderizarlo. ¿Será muy complicado juntar ambos?

.. _Qt: https://qt.io
.. _Emscripten: https://emscripten.org/index.html


**Nota.- La documentación recomienda utilizar versiones de las diferentes herramientas
que hayan sido probadas conjuntamente y se sepa que funcionan. En este blogpost seguiré
esta recomendación, aunque algunas otras combinaciones también me han funcionado.**

**Nota2.- El proceso ha sido probado en Macos, es esperable que en otros sistemas operativos
sea algo parecido. De cualquier forma, son bienvenidos los comentarios para actualizar esta
publicación e incluir más casos de uso.**

Emscripten
----------

El primer paso consiste en preparar Emscripten para compilar código C++ a Webassembly. El
proceso es muy sencillo y basta con seguir la `documentación`_ disponible en la web:

.. _documentación: https://emscripten.org/docs/getting_started/downloads.html

.. code-block:: bash

   git clone https://github.com/emscripten-core/emsdk.git
   cd emsdk
   git pull
   ./emsdk install 1.39.8
   ./emsdk activate 1.39.8

Esta versión de Emscripten utiliza también Python3 aunque no lo instala, versiones más
nuevas lo incluyen vendorizado. Suponemos que el lector si no lo tiene ya disponible en
el ``PATH`` sabe cómo conseguirlo.

En este proceso es importante notar el fichero ``emsdk_env.sh`` que ha sido generado
anteriormente. Este fichero es un **script para activar Emscripten como entorno de
desarrollo**, añadirá al ``PATH`` algunos directorios y variables de entorno para utlizar
los compiladores y herramientas que nos permitirán generan Webassembly.

Se recomienda al lector que pruebe algunos ejemplos básicos del `getting started`_
para verificar que el compilador funciona y tener una primera experiencia con el proceso.

.. _getting started: https://emscripten.org/docs/getting_started/Tutorial.html

Qt
--

El siguiente paso es compilar Qt para Webassembly. En realidad lo que haremos es compilar
para nuestro sistema operativo el _build-system_ ``qmake`` configurado como _cross_-compilador
que utiliza Webassembly como _target_. Suena más complicado de lo que es, podemos seguir
los pasos `este tutorial`_.

.. _este tutorial: https://doc.qt.io/qt-5/wasm.html

En primer lugar deberemos activar Emscripten como indicamos anteriormente:

.. code-block:: bash

   source emsdk/emsdk_env.sh
   emcc -v

Y descargar y compilar Qt para Webassembly:

.. code-block:: bash

   wget http://download.qt.io/official_releases/qt/5.15/5.15.2/single/qt-everywhere-src-5.15.2.tar.xz
   xz -d qt-everywhere-src-5.15.2.tar.xz
   tar xopf qt-everywhere-src-5.15.2.tar

   cd qt-everywhere-src-5.15.2
   ./configure -xplatform wasm-emscripten -nomake examples -nomake tests -prefix $(pwd)/qtbase
   make -j16 module-qtbase module-qtdeclarative

El proceso anterior tomará su tiempo, aprovecha para repasar algún ejemplo con Emscripten o refrescar
tus conocimientos de Qt. Tal vez sea un buen momento para buscar un ``Hello World!`` sencillo y ver cómo
funciona `qmake` con los ficheros `.pro` para generar las aplicaciones de Qt. Será útil en lo que viene
a continuación.

Una vez terminado el proceso anterior debería haberse generado **el ejecutable ``qtbase/bin/qmake``, éste
es nuestro _build-system_ preparado para cross-compilar utilizando Emscripten**.

Si creaste ese pequeño ``Hello world!``, ahora es el momento de comprobar que todo funciona. Dentro de su
directorio sólo tienes que ejecutar:

.. code-block:: bash

   cd hello-world
   .../qtbase/bin/qmake
   make

Ahora no tienes más que abrir el fichero ``.html`` con tu navegador de cabecera. Voilá! Lo que antes
era una aplicación de escritorio se ha convertido en una applicación web. El mismo código en C++ lo
hemos utilizado para generar una aplicación para dos plataformas totalmente diferentes... esto abre
un **horizonte de posibilidades**.


Aplicación
----------

Usando Conan
------------