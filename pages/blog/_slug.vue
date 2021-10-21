<template>
  <article class="flex flex-col gap-4">
    <h1 class="text-4xl">{{ article.title }}</h1>
    <div class="flex justify-start gap-2">
      <div class="text-gray-500">{{ formatDate(article.date) }}</div>
      <div
        class="px-3 py-1 text-xs text-white bg-gray-300 rounded-full"
        v-for="tag of article.tags"
        :key="tag"
      >
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
      .sortBy("date", "asc")
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

<style>
.nuxt-content p {
  margin-bottom: 20px;
}
.nuxt-content h2 {
  font-weight: bold;
  font-size: 28px;
}
.nuxt-content h3 {
  font-weight: bold;
  font-size: 22px;
}
.icon.icon-link {
  background-image: url("~assets/svg/icon-hashtag.svg");
  display: inline-block;
  width: 20px;
  height: 20px;
  background-size: 20px 20px;
}
.nuxt-content-highlight {
  @apply relative;
}
.nuxt-content-highlight .filename {
  @apply absolute right-0 text-gray-600 font-light z-10 mr-2 mt-1 text-sm;
}
.nuxt-content p code {
  @apply bg-gray-100 !important;
}
.nuxt-content p a {
  @apply text-red-500 hover:underline !important;
}
</style>
