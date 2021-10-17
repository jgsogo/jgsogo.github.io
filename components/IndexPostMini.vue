<template>
  <article class="flex flex-col gap-4">
    <h1 class="text-4xl">
      <NuxtLink :to="{ name: 'blog-slug', params: { slug: article.slug } }">
        {{ article.title }}
      </NuxtLink>
    </h1>
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
    <div>
      {{ article.description }}
    </div>
    <hr />
  </article>
</template>

<script>
export default {
  props: {
    article: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString("en", options);
    },
  },
};
</script>
