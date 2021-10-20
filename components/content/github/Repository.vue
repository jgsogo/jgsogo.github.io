<template>
  <span class="relative hover-trigger">
    <a :href="`https://github.com/${repo}/${link_internal}`">
      <slot>{{ repo }}</slot>
    </a>

    <p v-if="$fetchState.pending">Fetching info...</p>
    <p v-else-if="$fetchState.error">An error occurred :(</p>
    <span v-else
      class="absolute left-0 flex flex-col px-4 py-2 bg-white border rounded shadow -top-20 border-grey-100 hover-target"
    >
      <div>
        <a :href="info.owner.html_url">
          <img :src="info.owner.avatar_url" />
        </a>
        <strong>
          <a :href="info.html_url">{{ info.name }}</a>
          <sup>{{ info.language }}</sup>
        </strong>
      </div>
      <div>{{ info.description }}</div>
    </span>
  </span>
</template>

<script>
export default {
  props: {
    repo: {
      type: String,
      require: true,
    },
    link_internal: {
      type: String,
      default: () => "",
    },
  },
  data: () => ({
    info: null,
  }),
  async fetch() {
    console.log(`Getting data for repo: ${this.repo}`);
    this.info = (await this.$axios.get(`https://api.github.com/repos/${this.repo}`)).data;
    console.log(` - name: ${JSON.stringify(this.info.name)}`);
  },
  fetchKey: 'repo-card',
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
