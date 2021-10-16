<template>
  <article class="flex flex-col bg-yellow-100">
    <header>
      <h2 class="text-4xl">
        <NuxtLink :to="{ name: 'blog-slug', params: { slug: article.slug } }">
          {{ article.title }}
        </NuxtLink>
      </h2>
      <p class="text-sm text-gray-400">
        Posted on {{ formatDate(article.date) }} in {{ article.category }} ·
        Tagged with {{ article.tags.join(", ") }}
      </p>
    </header>
    <div>
      {{ article.description }}
    </div>
    <p>
      <NuxtLink :to="{ name: 'blog-slug', params: { slug: article.slug } }">
        Read...
      </NuxtLink>
    </p>
  </article>
</template>

<script>
export default {
  props: {
    article: {
      type: Object,
      default: () => null,
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
