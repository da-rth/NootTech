<template>
  <div id="download-container">
    <b-button class="download-btn">Download File ({{ file.file_size_str }})</b-button>
  </div>
</template>

<script>
    import BButton from "bootstrap-vue/src/components/button/button";

    export default {
      name: "DownloadFile",
      props: ['file'],
      components: {BButton}
    }
</script>

<style scoped>
  .download-container {
    width: 100%;
    margin: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  }
.download-btn {
  color: white;
  margin: 0 auto;
  mix-blend-mode: difference;
  padding: 10px 20px;
  background-color: #00CCCC;
}
</style>
