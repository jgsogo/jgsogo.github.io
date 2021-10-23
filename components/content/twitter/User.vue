<template>
  <a :href="`https://twitter.com/${user}`">
    <slot>@{{ user }}</slot>
  </a>
</template>

<script>
export default {
  props: {
    user: {
      type: String,
      require: true,
    },
  },
  data: () => ({
    info: null,
  }),
  async fetch() {
    this.info = {
        username: this.user
    }
  },
  fetchKey: "user-card",
};
</script>
