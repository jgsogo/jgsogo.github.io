<template>
  <div class="flex flex-col items-center justify-center p-4">
    <div
      class="inline-flex w-40 h-40 overflow-hidden border border-gray-200 rounded-full shadow-lg "
    >
      <img :src="person.image" :alt="person.name" class="w-full h-full" />
    </div>

    <h2 class="mt-4 text-xl font-bold">{{ person.name }}</h2>
    <h6 class="mt-2 text-sm font-medium">{{ person.role }}</h6>

    <p class="mt-3 text-xs text-center text-gray-500">
      {{ person.bio }}
    </p>

    <ul class="flex flex-row mt-4 space-x-2">
      <li v-if="person.social && person.social.github">
        <a
          :href="linkGithub(person.social.github)"
          class="flex items-center justify-center w-8 h-8 text-gray-800 border border-gray-800 rounded-full "
        >
          <fa-icon :icon="['fab', 'github']" />
        </a>
      </li>
      <li v-if="person.social && person.social.twitter">
        <a
          :href="linkTwitter(person.social.twitter)"
          class="flex items-center justify-center w-8 h-8 text-gray-800 border border-gray-800 rounded-full "
        >
          <fa-icon :icon="['fab', 'twitter']" />
        </a>
      </li>
      <li v-if="person.social && person.social.linkedin">
        <a
          :href="linkLinkedIn(person.social.linkedin)"
          class="flex items-center justify-center w-8 h-8 text-gray-800 border border-gray-800 rounded-full "
        >
          <fa-icon :icon="['fab', 'linkedin']" />
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
  methods: {
    linkTwitter(handle) {
      return `https://twitter.com/${handle}`;
    },
    linkGithub(handle) {
      return `https://github.com/${handle}`;
    },
    linkLinkedIn(handle) {
      return `https://www.linkedin.com/in/${handle}`;
    },
  },
};
</script>
