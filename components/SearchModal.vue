<!--
Follow here: https://dev.to/davidemaye/how-to-create-a-modal-component-in-nuxt-38g1
-->
<template>
  <div
    class="fixed top-0 bottom-0 left-0 right-0 flex justify-center bg-black bg-opacity-80"
    @click="doCloseModal"
  >
    <div
      class="w-1/2 p-20 mt-20 space-y-4 text-center bg-white bg-opacity-100 rounded h-1/3"
      @click.stop
    >
      <div class="mx-auto text-black">
        <input
          id="searchfield"
          v-model="searchQuery"
          type="search"
          placeholder="Search articles..."
          autofocus="autofocus"
          class="w-full py-2 text-xl leading-normal transition appearance-none text-grey-800 focus:outline-none focus:border-transparent lg:text-2xl"
        />
      </div>
      <hr>
      <div v-if="articles.length" class="flex flex-col space-y-4">
        <div
          v-for="article of articles"
          :key="article.slug"
          class="flex flex-row items-start space-x-2"
        >
          <span class="w-1/4 text-sm text-right text-gray-400">{{
            formatDate(article.date)
          }}</span>
          <span class="w-3/4 text-left" @click="doCloseModal"
            ><NuxtLink
              :to="{ name: 'blog-slug', params: { slug: article.slug } }"
            >
              {{ article.title }}
            </NuxtLink></span
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      articles: [],
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
  methods: {
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString("en", options);
    },
    doCloseModal() {
      //let searchfield = document.getElementById("searchfield");
      //searchfield.value = "";
      //this.articles = [];
      this.$emit("close-modal");
    },
  },
};
</script>

<style scoped>
.close {
  margin: 10% 0 0 16px;
  cursor: pointer;
}

.close-img {
  width: 25px;
}

.check {
  width: 150px;
}

h6 {
  font-weight: 500;
  font-size: 28px;
  margin: 20px 0;
}

p {
  font-size: 16px;
  margin: 20px 0;
}

button {
  background-color: #ac003e;
  width: 150px;
  height: 40px;
  color: white;
  font-size: 14px;
  border-radius: 16px;
  margin-top: 50px;
}
</style>
