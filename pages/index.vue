<template>
  <ul class="grid gap-10">
    <li v-for="article of articles" :key="article.slug">
      <index-post-mini :article="article"></index-post-mini>
      <hr />
    </li>
  </ul>
</template>

<script>
export default {
  layout: "blog",
  async asyncData({ $content, params }) {
    const articles = await $content("articles")
      //.only(['title', 'description', 'img', 'slug', 'author'])
      .sortBy("date", "asc")
      .fetch();

    return {
      articles,
    };
  },
};
</script>
