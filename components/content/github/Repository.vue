<template>
  <span class="relative hover-trigger">
    <a :href="`https://github.com/${repo}/${link_internal}`">
      <slot>{{ repo }}</slot>
    </a>

    <p v-if="$fetchState.pending">Fetching info...</p>
    <p v-else-if="$fetchState.error">An error occurred :(</p>
    <table
      v-else
      class="absolute left-0 z-50 grid grid-cols-3 px-2 py-2 bg-white border rounded shadow w-96 border-grey-100 hover-target"
    >
      <tbody class="">
        <tr>
          <td class="w-1/5">
            <a :href="info.owner.html_url">
              <img class="rounded" :src="info.owner.avatar_url" />
            </a>
          </td>
          <td class="flex flex-col align-top">
            <div>
              <strong>
                <a :href="info.html_url">{{ info.full_name }}</a>
              </strong>
              <img class="inline h-4" :src="`/icons/${info.language}.png`" />
            </div>
            <div class="text-sm text-gray-400">
              Created by
              <a :href="info.owner.html_url"
                ><span class="font-bold text-gray-600"
                  >@{{ info.owner.login }}</span
                ></a
              >
            </div>
          </td>
        </tr>
        <tr>
          <td colspan="2">
            {{ info.description }}
          </td>
        </tr>
        <tr>
          <td class="text-xs uppercase" colspan="2">
            <hr />
            <div class="pt-2">
              <div>
                <fa-icon :icon="['fab', 'github']" />
                <span class="font-bold">{{ info.forks }}</span> forks
                <span class="font-bold">{{ info.watchers }} </span> stars
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
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
  fetchKey: "repo-card",
};
</script>

<style>
.hover-trigger .hover-target {
  display: none;
}

.hover-trigger:hover .hover-target {
  display: block;
}

.hover-target td {
  padding: 4px;
}
</style>
