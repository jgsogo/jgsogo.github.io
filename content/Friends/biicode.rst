Biicode (como empresa) detiene su andadura
==========================================

:date: 2015-08-11 19:00
:tags: startup, diegorlosada
:slug: biicode-ends


Hoy Diego_ ha publicado el `cese de actividad de Biicode`__ como empresa. Y yo me quedo con una sensación de vacío y como pensativo.

.. _Diego: https://twitter.com/diegorlosada

__ http://blog.biicode.com/biicode-just-the-company-post-mortem/


.. figure:: {filename}/images/biicode.png
   :align: center
   
Biicode **cubre** un problema importante que no hemos sido capaces de abordar los programadores de C++ hasta ahora: la reutilización de código. Somos muy malos reutilizando el trabajo que han hecho otros. Yo mismo tengo que hacer un esfuerzo consciente importante para huir del copy/paste en favor de la creación de librerías, especialmente cuando se trata de pequeñas funcionalidades.

Cuando empiezas a utilizar Linux quedas fascinado por la genialidad que es aptitude_, cómo se instalan las cosas descargándose el código fuente y compilándose en tu ordenador reutilizando otras librerías que ya tienes instaladas. Luego aprendes Python y conoces Pypi_ y te convences de que algo así es necesario para que C++ sea un lenguaje de masas.

.. _aptitude: https://es.wikipedia.org/wiki/Aptitude
.. _Pypi: https://pypi.python.org/pypi

A medida que vas aprendiendo cosas descubres CMake_, y si eres perseverante terminas encontrando la función ExternalProject_Add_ y crearás `macros para gestionar con facilidad tus propios repositorios`__.

.. _CMake: http://www.cmake.org/
.. _ExternalProject_Add: http://www.cmake.org/cmake/help/v3.0/module/ExternalProject.html
__ https://github.com/jgsogo/cmake/blob/master/jgsogo_install.txt


---

Y entonces conoces Biicode_, un gestor de paquetes para C++, cuando aún lo están desarrollando y quizá terminando de definir el concepto. Y te enamoras de la idea. Y sólo lamentas no haberla conocido antes.

.. _Biicode: https://www.biicode.com/

.. figure:: {filename}/images/biicode_father.png
   :align: center
   :alt: Biicode. I'm your father
   
Te pones a utilizarla y encuentras ciertas dificultades, quizá más porque pretendes hacer las cosas a tu manera en vez de adaptarte a su flujo de trabajo. Hablando con Diego te das cuenta de que está orientada a entornos de trabajo donde la plantilla no son programadores puros, sino a equipos donde la programación es la herramienta para desarrollar proyectos, a *programadores* industriales. Ése es el entorno donde Biicode podía entrar comercialmente, pero quizá un entorno reacio y sin cultura de reutilización (ni de programación) suficiente como para identificar la necesidad.

Para los programadores profesionales Biicode **es** una herramienta estupenda para gestionar librerías y dependencias, aunque he de confesar que yo tendí más a seguir utilizando CMake directamente que Biicode... quizá iban demasiado rápido en sus versiones (la última vez que lo probé había algún problema con xml_parser_ y/o txt_table_ que prometo solucionar este año que estaré más liberado), o quizá su público objetivo en las redes sociales sobrepasaba mis conocimientos de programación, o simplemente puede que mis intereses se orientaran últimamente más hacia temas de Inteligencia Artificial que hacia temas puros de programación.

.. _xml_parser: https://github.com/jgsogo/xml_parser
.. _txt_table: https://github.com/jgsogo/txt_table

Sea como fuere, durante semanas he mantenido en la cabeza el pensamiento de *forzar* un encuentro con Diego para preguntarle cómo iba esa última ronda de financiación, y ya ves, lo vas dejando y dejando y terminas **enterándote por la prensa**.

---

Quiero terminar agradeciendo a Diego su esfuerzo en el desarrollo de Biicode y por supuesto también al resto de su equipo. **¡Confío en que el producto perviva!** Ya en lo personal, quiero resaltar la confianza y el tiempo que Diego me brindó, han supuesto para mí un hito importante. @Diego, aún sabiendo el desenlace, me hubiera gustado aceptar una oferta.



