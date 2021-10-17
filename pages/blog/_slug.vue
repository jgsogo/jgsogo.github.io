<template>
  <article class="flex flex-col gap-4">
    <h1 class="text-4xl ">{{ article.title }}</h1>
    <div class="flex justify-start gap-2">
      <div class="text-gray-500">{{ formatDate(article.date) }}</div>
      <div class="px-3 py-1 text-xs text-white bg-gray-300 rounded-full" v-for="tag of article.tags" :key="tag">
      {{ tag }}
      </div>
    </div>
    <nuxt-content :document="article" />

    <hr />
    <prev-next :prev="prev" :next="next" />
  </article>
</template>

<script>
export default {
  layout: "blog",
  async asyncData({ $content, params }) {
    // fetch our article here
    console.log(`blog/_slug: ${JSON.stringify(params)}`);
    const article = await $content("articles", params.slug).fetch();

    const [prev, next] = await $content("articles")
      .only(["title", "slug"])
      .sortBy("createdAt", "asc")
      .surround(params.slug)
      .fetch();

    return {
      article,
      prev,
      next,
    };
  },
  methods: {
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString("en", options);
    },
  },
};
</script>
