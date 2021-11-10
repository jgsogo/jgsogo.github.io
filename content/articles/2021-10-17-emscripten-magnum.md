---
lang: en
title: Magnum example using Emscripten
date: 2021-10-17
author: jgsogo
category: C++
tags: 
  - c++
  - wasm
  - emsdk
  - magnum
  - conan
description: |
  In this article I use Emscripten to render an STL model in the browser with 
  the help of Magnum library. I'll use Conan and packages from ConanCenter to
  get the libraries and build everything needed. Finally we will get the files
  we need to deploy in a web server to interact with the 3D model.
draft: true
---


Some months ago I joined a 3D course using Blender. The main purpose was to
recover this hobby I enjoyed a lot in the good old days, but soon my mind started
to think about showing those 3D models in the browser. Using C++, of course.
Spoiler: I didn't finish the course.

<!--more-->

Anyway, before moving forwards, I want to show you the viking shield I managed
to do in the first lessons. I really enjoyed it and I can only recommend all the
courses that 
<content-twitter-user user="par_virtual">Pablo</content-twitter-user> 
and <content-twitter-user user="KoreFormacion">Koré team</content-twitter-user>
will organize in the future.

<article-image src="/img/2021/kore-shield.png" alt="Viking shield" caption="Viking shield recreation"></article-image>


## Looking for alternatives 

When it comes to web and C++ there are not too many options
out there. So far I can only think about
<nuxt-link to="/blog/2021-01-19-emscripten-cube">Qt</nuxt-link> and
[Wt](https://www.webtoolkit.eu/wt), any other alternative would involve dealing
with HTML and CSS. In this case I didn't want a fully featured application, I
just wanted to render some 3D.

For this example I was going to need some graphics library able to import the
3D data and the corresponding graphic engine to render it. There are many
libraries that satisfies these two requirements (it remembers me two years ago
when for some reason lot of people from the C++ community started to build their own 
[raytracing implementation](https://manu343726.github.io/2019-06-20-raytracer-runtime-postmortem/)),
but when you start to search for 3D and web, and you add Emscripten to the equation
the alternatives are narrowed. In fact, I only found [Magnum](https://magnum.graphics/)
satisfying all these requirements.


### Magnum libraries

Magnum looked like a good approach: modern library, active development, modular architecture,
plugins,... with a lot of examples showcasing different examples built using Emscripten.

<article-image 
  src="/img/2021/magnum-features.png" 
  alt="Magnum features chart" 
  caption="Magnum architecture is organize into layers that add functionality on top of each other. The foundation are the core libraries that provides some platform abstraction and very basic features. On top of these layers, some extra modules contribute with actual functionaliy for different use-cases. This architecture makes it easy to contribute new modules and extensions.">
</article-image>

For this example I just needed to build the core libraries with some OpenGL (WebGL)
support, and the required components to import my 3D models. Anyway, those were
a bunch of libraries using different build systems.


## Building the libraries

**Magnum project** is quite good at documentation, and a lot of attention has been paid to
the build system. Magnum provides good and modern `CMakeLists.txt` files and every single
option is [exhaustively documented](https://doc.magnum.graphics/magnum/building.html#building-manual).

The core library `Magnum` depends only on a bunch of third party libraries, and some of them are
optional depending on the active features. Many other libraries are required if we start to add
plugins related to other features: mesh importers, fonts, images, sound,...

<article-image 
  src="/img/2021/magnum-deps.png" 
  alt="Magnum direct dependencies" 
  caption="Magnum direct dependencies.">
</article-image>

There are plenty of plugins in the 
<content-github-repository repo="mosra/magnum-plugins">magnum-plugins</content-github-repository>
repository. I won't need all of them, but the following graph shows the third party libraries
that are required if we want to activate them. Of course, for this little example we don't need
all of them, they are just listed here for completeness.

<article-image 
  src="/img/2021/magnum-plugins-deps.png" 
  alt="Magnum plugins direct dependencies" 
  caption="Magnum plugins dependencies.">
</article-image>

If you have some experience with C++ ecosystem, soon you will think that these are too many
libraries and it will be very challenging to build all of them from sources. Thankfully, some
of them can be installed at system level using the system package manager or similar tools.
Nevertheless this would introduce some limitations and compatibility issues, but this is not
the place to talk about it.

Given all these libraries I decided to approach the problem using a package manager. Of course,
the choosen one was [Conan](https://conan.io) (I work in the project). Thanks to the community
effort most of the libraries were already available in [ConanCenter](https://conan.io/center),
but still there were some missing libraries.

### Conanize all the things 

It took some time to create all the missing recipes and improve existing ones to be able to
_conanize_ all the libraries in the Magnum graph, but hopefully this effort is worth it and
other people from the community will benefit from it.

In [this issue](https://github.com/conan-io/conan-center-index/pull/6292) you can find most of
the changes that were required to add `magnum/2020.06` to ConanCenter. As you can see it took me
around three months to contribute all the changes and there are still some missing improvements,
mostly related to Emscripten, but it's not clear to me how to address them in the context
of <content-github-repository repo="conan-io/conan-center-index">conan-center-index</content-github-repository>
repository.

Of course, it hasn't been only my work, but the effort of several contributors from the community that
helped me creating other recipes. Thanks and kudos to all of them.

## Emscripten



### Magnum and SDL

## Reproducible steps

## Enjoy!

---

aaaa <content-github-repository repo="jgsogo/blog-20211008-example-emsdk-magnum"></content-github-repository>aaa


<content-magnum-wasm base_path="https://jgsogo.es/blog-20211008-example-emsdk-magnum" caption="Use controls..."></content-magnum-wasm>
