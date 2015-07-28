Title: Mi primer paquete en PyPI
Date: 2015-07-29 10:20
Tags: pypi, apicultur
Slug: first-package-pypi


Nadie tiene dudas de que [PyPI](https://pypi.python.org/pypi) es una de las joyas de Python, el simple hecho
de tener a tu alcance infinitud de librerías con sólo escribir `pip install library` lo convierte en una
herramienta tremendamente útil y probablemente sea una de las razones del éxito de Python entre los que
empiezan a programar.

Así que para el proyecto que estamos lanzando, [Lingẅars](http://lingwars.github.io/blog/),
donde participa gente con poca experiencia
en programación resulta prácticamente necesario enpaquetar el código que vamos a utilizar y subirlo al
gestor de paquetes para que puedan empezar a ejecutar ejemplos desde el primer día.

Con este objetivo he creado el paquete `apicultur` ([PyPI](https://pypi.python.org/pypi/apicultur),
[source](https://github.com/jgsogo/apicultur-python)) para acceder a las APIs lingüísticas de
[Apicultur](https://apicultur.io/). Por supuesto, te lo puedes instalar escribiendo:

```bash
   pip install apicultur
```

Este _tutorial_ está inspirado en estos posts de [Tom Christie](https://tom-christie.github.io/articles/pypi/),
[Jamie Curle](https://jamie.curle.io/posts/my-first-experience-adding-package-pypi/) y la documentación de la
propia [Python Foundation](https://packaging.python.org/en/latest/distributing.html); cualquier duda que te
surja seguro que está resuelta ahí, yo sólo intentaré ser breve e ir a lo imprescindible.


## Estructura mínima
Para poder empaquetar una librería necesitamos como mínimo la siguiente estructura de archivos:

```
DIRECTORIO-DEL-PROYECTO
├── setup.py
├── NOMBRE-DEL-PAQUETE
     ├── __init__.py
     ├── FILE1.py
     ├── FILE2.py
     └── MODULE (OPCIONAL)
           ├── __init__.py
           └── MOREFILES.py
```

Vamos a ver qué significan los elementos anteriores:

 * el DIRECTORIO-DEL-PROYECTO puede ser cualquiera, no afecta en absoluto, lo que cuenta es lo que hay dentro.
 * NOMBRE-DEL-PAQUETE tiene que ser el nombre del paquete, si el nombre es `apicultur`, este directorio tiene
   que llamarse también `apicultur`. Y esto es así. Dentro estarán todos los archivos que forman la librería.
 * `setup.py`: es el archivo donde se define el paquete, el formato es el mismo para `setuptools` y para
   `distutils` así que no hay que preocuparse por nada más. Lo vemos a continuación.

## setup.py
Este archivo, con toda la información del paquete, tiene que tener un contenido parecido al siguiente:

```python
    from setuptools import setup, find_packages
    from os import path

    setup(
        name='NOMBRE-DEL-PAQUETE',
        version='0.1.10',
        description='A sample Python project',
        long_description='More information about the sample project',
        url='https://github.com/whatever/whatever',
        author='yourname',
        author_email='your@address.com',

        license='MIT',

        # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            'Operating System :: OS Independent',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
        ],

        keywords='sample setup',
        packages=find_packages(),
        install_requires=['requests', 'more-deps',],  #
    )
```

## Subiendo el código a PyPI
Verifica primero que el archivo es correcto:

```bash
   $ python setup.py test
```

Y ahora ya puedes generar los archivos que van a distribuirse en PyPI:

```bash
   $ python setup.py sdist
```

Este comando crea un archivo comprimido con todos lo que va a subirse al gestor de paquetes PyPI, este
archivo se guarda en un directorio `dist/` que habrá sido creado en el directorio de tu proyecto (si estás utilizando
un gestor de versiones acuérdate de añadir este directorio a los archivos ignorados).

Vas a necesitar un usuario en PyPI para poder subir el paquete; una vez que lo tengas puedes registrar el
paquete utilizando el formulario que hay en la web o bien directamente con

```bash
    $ python setup.py register
```

Este registro sólo lo tendrás que realizar una vez.

Una vez que el paquete está registrado puede subir cada nueva versión (también la primera) utlizando `twine`:

```bash
    $ pip install twine
    $ twine upload dist/NOMBRE-DEL-PAQUETE-VERSION.tar.gz
```

Y ya está listo para ser utilizado.


## Otras recomendaciones
En este tutorial hemos ido a lo imprescindible, pero para que un paquete sea realmente reutilizable y que
su mantenimiento no resulte una tarea titánica es muy recomendable seguir también otras recomendaciones:

 * Escribe tests.
 * Usa algún sistema de integración continua que ejecute esos tests automáticamente.
 * ¡Documenta!
 * ¡Y mantén la documentación actualizada!

____

### Enlaces de interés
 * Reutilización de código en C++: hecha un vistazo a [BiiCode](https://www.biicode.com/) ;D
