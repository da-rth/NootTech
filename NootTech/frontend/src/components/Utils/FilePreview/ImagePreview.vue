<template>
  <div id="NTImagePreview">
      <img id="NTImage" :src="$site_url+file.file_content">
  </div>
</template>

<script>
    export default {
        name: "ImagePreview",
        props: ['file'],
    }
</script>

<style scoped>
#NTImagePreview {
  width: 100%;
     background-color: #181818;
    border-top: 1px solid rgba(0,0,0,0.6);
    border-bottom: 1px solid rgba(0,0,0,0.6);
}
  #NTImage {
    padding: 30px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-height: 60vh;
    max-width: 70vw;
  }
</style>
