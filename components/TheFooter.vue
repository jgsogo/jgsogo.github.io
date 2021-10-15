<template>
  <div class="flex justify-center bg-gray-100">
    © Javier G. Sogo {{ currentYear }}
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentYear: new Date().getFullYear(),
    };
  },
};
</script>