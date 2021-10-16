<template>
  <div class="flex w-full">
    <div class="w-1/4 bg-yellow-100">
      <div class="fixed w-1/4 top-20">
        <ul class="float-right text-right">
          <li class="px-3 space-x-2">
            <fa-icon :icon="['fa', 'home']" /><span>Home</span>
          </li>
          <!--<li class="space-x-2" type="button" onclick="startSearch()"><fa-icon :icon="['fa', 'search']" /><span>Search</span></li>-->
          <li class="px-3 space-x-2">
            <AppSearchInput />
          </li>
        </ul>
      </div>
      <div class="fixed bottom-0 flex flex-col w-1/4 bg-yellow-400">
        <data-person :person="owner"></data-person>
      </div>
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
  methods: {
    startSearch() {
      console.log("HEY!");
    },
  },
};
</script>
