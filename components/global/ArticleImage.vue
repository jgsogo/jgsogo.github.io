
<template>
  <figure class="p-4">
    <img :src="src" :alt="alt" class="flex-grow article-image" />
    <div v-if="source" class="text-xs text-right">Source: {{ source }}</div>
    <figcaption v-if="caption" class="p-2 text-sm text-center">
      <i>{{ caption }}</i>
    </figcaption>
  </figure>
</template>


<script>
export default {
  props: {
    src: {
      type: String,
      required: true,
    },
    alt: {
      type: String,
      required: true,
    },
    caption: {
      type: String,
      default: () => null,
    },
    source: {
      type: String,
      default: () => null,
    },
  },
};
</script>
