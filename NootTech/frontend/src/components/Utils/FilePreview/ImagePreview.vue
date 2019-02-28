<template>
  <div id="NTImagePreview">
      <img id="NTImage" :src="image">
  </div>
</template>

<script>
    export default {
        name: "ImagePreview",
        props: ['file'],
        data() {
        return {
          image: this.file.file_content.startsWith('/') ? this.$backend_url+this.file.file_content : this.file.file_content
        }
    },
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
