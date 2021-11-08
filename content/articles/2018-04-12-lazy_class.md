---
lang: es
title: Métodos lazy (opcionales) en una clase
date: 2018-04-13
author: jgsogo
category: Python
tags: 
  - python
  - lazy
  - snippet
---

Este post es un **apunte rápido** para documentar una implementación de funciones ``lazy`` a través de
decoradores en una clase de Ptyhon. La idea es tener una forma sencilla de definir funciones de
una clase que:

* se puedan ejecutar tan pronto como se crea un objeto (o no),
* almacenen en caché el resultado de la función.

<!--more-->

Esta implementación puede ser útil en el contexto de clases cuyo objetivo es parsear archivos
de texto pesados. La ejecución inmediata permita conocer tan pronto como sea posible si hay
algún error en el formato.

Las piezas necesarias para montarlo son:

* Un decorador:

    ```python

    class lazy(object):

        def __init__(self, func):
            self.func = func
            self.lazy_keyword = '__{}'.format(func.__name__)

        def __call__(self, *args, **kwargs):
            log.warning("Do not use @lazy for free functions like '{}'. Did you intend @memoize?".format(self.func.__name__))
            return self.func(*args, **kwargs)

        def __get__(self, inst, cls=None):
            if inst is not None:
                def wrapped_func(*args, **kwargs):
                    if not hasattr(inst, self.lazy_keyword):
                        # setattr(inst, self.lazy_keyword, self.func(inst, *args, **kwargs))
                        setattr(inst, self.lazy_keyword, types.MethodType(self.func, inst, cls)(*args, **kwargs))
                    return getattr(inst, self.lazy_keyword)
                return wrapped_func
            else:
                return self

        def init_cls(self, name, cls):
            assert issubclass(cls, LazyMixin), "Use @lazy for member functions of classes that inherit from LazyMixin"

            def wrapped_func(inst, *args, **kwargs):
                if not hasattr(inst, self.lazy_keyword):
                    # setattr(inst, self.lazy_keyword, self.func(inst, *args, **kwargs))
                    setattr(inst, self.lazy_keyword, types.MethodType(self.func, inst, cls)(*args, **kwargs))
                return getattr(inst, self.lazy_keyword)

            cls._lazy_functions.append(wrapped_func)
    ```

* Una metaclase:
 
    ```python

    class MetaLazy(type):

        def __init__(cls, name, bases, classdict):
            if name != 'LazyMixin':
                cls._lazy_functions = []

            # getmembers retrieves all attributes
            # including those inherited from parents
            for k, v in inspect.getmembers(cls):
                if isinstance(v, lazy):
                    v.init_cls(k, cls)
    ```

* Una clase base:
 
    ```python

    class LazyMixin(object):
        __metaclass__ = MetaLazy

        _lazy_functions = []

        def invoke_lazy_functions(self):
            for func in self._lazy_functions:
                func(self)
    ```
    
Apoyándose en esto, uno puede definir clases que tengan funciones `lazy`:

```python

class ALazyClass(LazyMixin):

    def __init__(self, lazy=True, *args, **kwargs):
        if not lazy:
            self.invoke_lazy_functions()

    @lazy
    def lazy1(self):
        print("return 23")
        return 23
```

...espero volver pronto por aquí para mejorar este apunte.
