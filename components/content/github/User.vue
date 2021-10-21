<template>
  <a :href="`https://github.com/${user}`">
    <slot>{{ user }}</slot>
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
    console.log(`Getting data for user: ${this.user}`);
    this.info = (
      await this.$axios.get(`https://api.github.com/users/${this.user}`)
    ).data;
  },
  fetchKey: "user-card",
};
</script>
