<template>
  <span class="hover-trigger">
    <a :href="`https://github.com/${repo}`">
      <slot>{{ repo }}</slot>
    </a>
    <span
      class="absolute px-4 py-2 bg-white border rounded shadow border-grey-100 hover-target"
    >
    {{ info.description }}
    </span>
  </span>
</template>

<script>
import axios from "axios"; // don't forget me!

export default {
  props: {
    repo: {
      type: String,
      require: true,
    },
  },
  data: () => ({
    info: null,
  }),
  async fetch() {
    console.log(`Getting data for repo: ${this.repo}`);
    this.info = (await axios.get(`https://api.github.com/repos/${this.repo}`)).data;
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

