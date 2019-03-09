<template>
  <div id="NTImagePreview" :file=file @input="$emit('input', $event.target.file)">
      <img id="NTImage" :src="image">
  </div>
</template>

<script>
export default {
  name: "ImagePreview",
  props: ['file'],
  model: {
    prop: "file",
    event: "input"
  },
  computed: {
    image() {
      return this.file.file_content.startsWith('/') ?
             this.$backend_url+this.file.file_content :
             this.file.file_content
    },
  },
  mounted() {
      console.log("Hello from ImagePreview");
  }
}
</script>

<style scoped>
#NTImagePreview {
  overflow: hidden;
  width: 100%;
  background-color: #181818;
  border-top: 1px solid rgba(0,0,0,0.6);
  border-bottom: 1px solid rgba(0,0,0,0.6);
}
#NTImage {
  display: block;
  margin-left: auto;
  margin-right: auto;
  width: 100%;
}
</style>
