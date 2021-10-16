<template>
  <div
    class="flex flex-col items-center justify-center p-4 bg-white rounded-lg shadow "
  >
    <div
      class="inline-flex w-40 h-40 overflow-hidden border border-gray-200 rounded-full shadow-lg "
    >
      <img :src="author.image" :alt="author.name" class="w-full h-full" />
    </div>

    <h2 class="mt-4 text-xl font-bold">{{ author.name }}</h2>
    <h6 class="mt-2 text-sm font-medium">{{ author.role }}</h6>

    <p class="mt-3 text-xs text-center text-gray-500">
      {{ author.bio }}
    </p>

    <ul class="flex flex-row mt-4 space-x-2">
      <li>
        <a
          href=""
          class="flex items-center justify-center w-8 h-8 text-gray-800 border border-gray-800 rounded-full "
        >
          <i class="fab fa-facebook"></i>
        </a>
      </li>
      <li>
        <a
          href=""
          class="flex items-center justify-center w-8 h-8 text-gray-800 border border-gray-800 rounded-full "
        >
          <i class="fab fa-twitter"></i>
        </a>
      </li>
      <li>
        <a
          href=""
          class="flex items-center justify-center w-8 h-8 text-gray-800 border border-gray-800 rounded-full "
        >
          <i class="fab fa-instagram"></i>
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    author: {
      type: Object,
      required: true,
    },
  },
};
</script>
