<template>
  <span class="relative hover-trigger">
    <a :href="`https://github.com/${repo}/${link_internal}`">
      <slot>{{ repo }}</slot>
    </a>
    <span
      class="absolute left-0 flex flex-col px-4 py-2 bg-white border rounded shadow -top-20 border-grey-100 hover-target"
    >
      <pre>{{ info }}</pre>
      <div>
        <a href="info.owner.html_url">
          <!--<img src="info.owner.avatar_url" />-->
        </a>
        <strong>
          <a href="info.html_url">info.name</a>
          <sup> info.language</sup>
        </strong>
      </div>
      <div>info.description</div>
      <div></div>
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
    this.info = (await axios.get(`https://api.github.com/repos/${this.repo}`)).data;
    console.log(` - name: ${JSON.stringify(this.info)}`);
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
