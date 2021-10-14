<template>
  <article>
    <AppSearchInput />

    <nav>
      <ul>
        <li
          v-for="link of article.toc"
          :key="link.id"
          :class="{
            'font-semibold': link.depth === 2,
          }"
        >
          <nuxtLink
            :to="`#${link.id}`"
            class="hover:underline"
            :class="{
              'py-2': link.depth === 2,
              'ml-2 pb-2': link.depth === 3,
            }"
            >{{ link.text }}</nuxtLink
          >
        </li>
      </ul>
    </nav>

    <h1>{{ article.title }}</h1>
    <p>{{ article.description }}</p>
    <img :src="article.img" :alt="article.alt" />
    <p>Post last updated: {{ formatDate(article.updatedAt) }}</p>
    <author :author="article.author" />
    <nuxt-content :document="article" />
    <prev-next :prev="prev" :next="next" />
    <!--
    <hr />
    <pre> {{ article }} </pre>
    -->
  </article>
</template>

<script>
export default {
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
