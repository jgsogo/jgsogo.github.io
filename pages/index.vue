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
      .where({
        draft: {
          $in: [undefined, false],
        },
      })
      //.only(['title', 'description', 'img', 'slug', 'author'])
      .sortBy("date", "desc")
      .fetch();

    return {
      articles,
    };
  },
};
</script>
