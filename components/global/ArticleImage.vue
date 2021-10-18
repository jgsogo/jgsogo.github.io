
<template>
  <div>
    <img :src="src" :alt="alt" class="article-image" />
    <span v-if="caption">{{ caption }}</span>
  </div>
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
  },
};
</script>
