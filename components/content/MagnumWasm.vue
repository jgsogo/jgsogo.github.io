<template>
  <div class="m-0">
    <div class="w-full">
      <div class="mn-expander">
        <div class="mn-listener">
          <canvas class="w-full" id="canvas"></canvas>
          <div class="mn-status" id="status">Initialization...</div>
          <div class="mn-status-description" id="status-description"></div>
          <script :src="`${base_path}/EmscriptenApplication.js`"></script>
          <script async="async" :src="`${base_path}/viewer.js`"></script>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    base_path: {
      type: String,
      require: true
    }
  }
}
</script>
