<template>
  <div>
    
    <!--Search-->
    <div
      class="fixed top-0 left-0 hidden w-full bg-white shadow-xl"
      id="search-content"
    >
      <div class="mx-auto text-black">
        <input
          id="searchfield"
          v-model="searchQuery"
          type="search"
          placeholder="Search..."
          autofocus="autofocus"
          class="w-full py-2 text-xl leading-normal transition appearance-none text-grey-800 focus:outline-none focus:border-transparent lg:text-2xl"
        />
      </div>
      <ul v-if="articles.length">
        <li v-for="article of articles" :key="article.slug">
          <NuxtLink :to="{ name: 'blog-slug', params: { slug: article.slug } }">
            {{ article.title }}
          </NuxtLink>
        </li>
      </ul>
    </div>

    <div
      id="search-toggle"
      class="space-x-2 cursor-pointer"
      @click="$emit('show-search-modal')"
      v-on:click="doShowModal"
    >
      <fa-icon :icon="['fa', 'search']" /><span>Search</span>

      <!--
      <fa-icon :icon="['fa', 'search']" />
      <input
        class="w-16 text-black bg-transparent border-none"
        v-model="searchQuery"
        type="search"
        autocomplete="off"
        placeholder="Search"
      />
      -->
    </div>

    <!--
    <ul v-if="articles.length">
      <li v-for="article of articles" :key="article.slug">
        <NuxtLink :to="{ name: 'blog-slug', params: { slug: article.slug } }">
          {{ article.title }}
        </NuxtLink>
      </li>
    </ul>
    -->
  </div>
</template>

<script>
import SearchModal from "~/components/SearchModal.vue";

export default {
  data() {
    return {
      searchQuery: "",
      articles: [],
      showModal: false,
    };
  },
  watch: {
    async searchQuery(searchQuery) {
      if (!searchQuery) {
        this.articles = [];
        return;
      }
      this.articles = await this.$content("articles")
        .limit(6)
        .search(searchQuery)
        .fetch();
    },
  },
  components: { SearchModal },
  methods: {
    doShowModal: function (e) {
      this.showModal = true;
    },
    searchToggle: function (event) {
      //var searchMenuDiv = this.$refs["search-content"];
      var searchMenuDiv = document.getElementById("search-content");
      if (searchMenuDiv.classList.contains("hidden")) {
        searchMenuDiv.classList.remove("hidden");
        searchfield.focus();
      } else {
        searchMenuDiv.classList.add("hidden");
      }
      console.log("test clicked");
    },
  },
};
</script>
