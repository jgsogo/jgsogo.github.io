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
---


Some months ago I joined a 3D course using Blender. The main purpose was to
recover this hobby I enjoyed a lot in the good old days, but soon my mind started
to think about showing those 3D models in the browser. Using C++, of course.
Spoiler: I didn't finish the course.

<!--more-->

Anyway, before moving forwards, I want to show you the viking shield I managed
to do in the first lessons. I really enjoyed it and I can only recommend all the
courses that 
<content-twitter-handle handle="par_virtual">Pablo</content-twitter-handle> 
and <content-twitter-handle handle="KoreFormacion">Koré team</content-twitter-handle>
will organize in the future.

<article-image src="/img/articles/kore-shield.png" alt="Viking shield" caption="Viking shield recreation"></article-image>


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
  src="/img/articles/magnum-features.png" 
  alt="Magnum features chart" 
  caption="Magnum architecture is organize into layers that add functionality on top of each other. The foundation are the core libraries that provides some platform abstraction and very basic features. On top of these layers, some extra modules contribute with actual functionaliy for different use-cases. This architecture makes it easy to contribute new modules and extensions.">
</article-image>

For this example I just needed to build the core libraries with some OpenGL (WebGL)
support, and the required components to import my 3D models. Anyway, those were
a bunch of libraries using different build systems.


## 

---

aaaa <content-github-repository repo="jgsogo/blog-20211008-example-emsdk-magnum"></content-github-repository>aaa


<content-magnum-wasm base_path="https://jgsogo.github.io/blog-20211008-example-emsdk-magnum" caption="Use controls..."></content-magnum-wasm>
