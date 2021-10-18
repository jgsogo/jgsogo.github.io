<template>
  <span class="hover-trigger">
    <a :href="`https://twitter.com/${handle}`">
      <slot>{{ handle }}</slot>
    </a>
    <span
      class="absolute px-4 py-2 bg-white border rounded shadow border-grey-100 hover-target"
    >
      Boo!
    </span>
  </span>
</template>

<script>
export default {
  props: {
    handle: {
      type: String,
      require: true,
    },
  },
  data: () => ({
  }),
  async fetch() {
    console.log(`Trying here: ${this.handle}`);
  },
};
</script>

<style>
.hover-trigger .hover-target {
  display: none;
}

.hover-trigger:hover .hover-target {
  display: block;
}
</style>

