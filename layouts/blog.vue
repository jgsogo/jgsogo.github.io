<template>
  <div class="flex w-full">
    <div class="w-1/4">
      <div class="fixed w-1/4 top-10">
        <ul class="float-right text-right">
          <li class="px-3 space-x-2">
            <NuxtLink :to="{ name: 'index' }"
              ><fa-icon
                :icon="['fa', 'home']"
              /><!--<span>Home</span>--></NuxtLink
            >
          </li>
          <li class="px-3 space-x-2 cursor-pointer" v-on:click="doShowModal">
            <fa-icon :icon="['fa', 'search']" /><!--<span>Search</span>-->
          </li>
          <li class="px-3 space-x-2 cursor-pointer">
            <a :href="`https://twitter.com/intent/tweet?text=${tweet_text}`" target="_blank">
              <fa-icon :icon="['fa', 'comment']" /><!--<span>Comment</span>-->
            </a>
          </li>
        </ul>
      </div>
      <div class="fixed flex flex-col w-1/4 bottom-20">
        <data-person :person="owner"></data-person>
      </div>
    </div>
    <div class="w-3/4">
      <div class="w-4/6">
        <!-- <TheHeader /> -->
        <div class="p-10">
          <Nuxt />
        </div>
        <!-- <TheFooter /> -->
      </div>
    </div>

    <SearchModal class="" v-show="showModal" @close-modal="showModal = false" />
  </div>
</template>

<script>
import { url, twitter } from "../utils/getSiteMeta";

export default {
  layout: "blog",

  data: () => ({
    owner: null,
    showModal: false,
    tweet_text: null,
  }),
  async fetch() {
    this.owner = await this.$content("authors", "jgsogo").fetch();
    this.tweet_text = `Hey ${twitter}! I've read ${url}${this.$route.path} and want to...`;
  },
  beforeMount() {
    window.addEventListener("keydown", this.onEscape);
  },
  beforeDestroy() {
    window.removeEventListener("keydown", this.onEscape);
  },

  methods: {
    doShowModal: function (e) {
      this.showModal = true;
      this.$nextTick(function () {
        let searchfield = document.getElementById("searchfield");
        searchfield.focus();
      });
    },
    onEscape: function (e) {
      if (this.showModal && e.keyCode === 27) {
        this.showModal = false;
      }
    },
  },
};
</script>

<style>
html {
  font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI",
    Roboto, "Helvetica Neue", Arial, sans-serif;
  font-size: 18px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
}
</style>
