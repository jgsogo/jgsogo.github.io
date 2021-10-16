<template>
  <card>
    <template #card-content>
      <data-person :person="person"></data-person>
    </template>
  </card>
</template>

<script>
export default {
  props: {
    person: {
      type: Object,
      required: true,
    },
  },
};
</script>
