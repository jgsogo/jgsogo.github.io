---
title: My first Blog Post
description: Learning how to use @nuxt/content to create a blog
img: typewriter.jpg
alt: my first blog post
author:
  name: Benjamin
  bio: All about Benjamin
  image: https://avatars.githubusercontent.com/u/1406456?v=4
---


## This is a heading

This is some more info

### This is a sub heading

This is some more info

### This is another sub heading

This is some more info

## This is another heading

This is some more info


```yaml[filename.yaml]
export default {
  nuxt: 'is the best'
}
```

<div class="p-4 mb-4 text-white bg-blue-500">
  This is HTML inside markdown that has a class of note
</div>

<info-box>
  <template #info-box>
    This is a vue component inside markdown using slots
  </template>
</info-box>
