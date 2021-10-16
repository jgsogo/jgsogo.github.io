<template>
  <div class="flex w-screen">
    <div class="flex flex-col w-1/4 bg-yellow-100">
      <author-card :author="owner"></author-card>
      <AppSearchInput />
    </div>
    <div class="w-3/4 bg-green-100">
      <div class="w-4/6">
        <TheHeader />
        <div class="p-10">
          <Nuxt />
        </div>
        <TheFooter />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: "blog",
  data: () => ({
    owner: null,
  }),
  async fetch() {
    this.owner = await this.$content("authors", "jgsogo").fetch();
  },
};
</script>
