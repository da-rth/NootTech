<template>

  <div id="HowTo" >
    <h1>Uploading through the command-line</h1>
    <p class="description">
      You can upload any of your files directly through the command-line using protocol software such as
      <a href="https://curl.haxx.se/">cURL</a>.
    </p>
    <highlight-code lang="bash">
    # You can upload files using cURL

    $ curl
    -F "username=Your_Username_Here"
    -F "upload_key=Your_Key_Here"
    -F "content=@/path/to/my/file.jpg"
    -F "content=@/path/to/my/second-file.jpg"
    {{ this.$site_url }}/api/upload
		</highlight-code>

    <br/>

    <h1>Uploading via ShareX</h1>
    <p class="description">
      <a href="https://getsharex.com/">ShareX</a> is a screen capturing, file sharing and productivity tool which can be used to upload your files and screenshots directly here!
    </p>
  </div>
</template>

<script>
  export default {
    name: "HowTo"
  }
</script>

<style>
#HowTo {
  margin: 0 auto;
  width: 84vw;
  height: 84vh;
  margin-top: 30px;
  padding: 30px;
}
.description {
  color: white;
}
</style>
