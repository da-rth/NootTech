<template>
  <div class="justify-content-center">
    <template v-if="this.file">

      <h2 class="file-header">{{ this.file.original_filename }}</h2>

      <VideoPlayer :file="file" v-if="file.file_video_info"/>
      <AudioPlayer :file="file" v-else-if="file.file_audio_info" class="AudioPlayerContainer"/>
      <ImagePreview :file="file" v-else-if="file.file_image_info"/>
      <TextPreview :file="file" v-else-if="file.file_text_info"/>

      <DownloadFile :file="file" />

      <h4 class="file-header">File Information</h4>
      <FileInformation :file="file"/>
    </template>
  </div>
</template>

<script>
  import VideoPlayer from "../Utils/FilePreview/VideoPlayer";
  import AudioPlayer from "../Utils/FilePreview/AudioPlayer";
  import DownloadFile from "../Utils/FilePreview/DownloadFile";
  import ImagePreview from "../Utils/FilePreview/ImagePreview";
  import TextPreview from "../Utils/FilePreview/TextPreview";
  import FileInformation from "../Utils/FilePreview/FileInformation";

  export default {
    name: "ShareLinkPage",
    data () {
      return {
        file: null,
        colour: null,
        username: null,
        gen_name: null,
      }
    },
    components: {
      TextPreview,
      ImagePreview,
      DownloadFile,
      AudioPlayer,
      VideoPlayer,
      FileInformation
    },

    async beforeMount() {

        this.username = this.$route.params.username;
        this.gen_name = this.$route.params.gen_name;
        this.$root.sharelinkName = this.username;

        await this.$api.GetShareData(this.username, this.gen_name)
        .then(response => {
          console.log("SHARELINK SUCCESS", response)
          this.file = response.data.file;
          this.$root.colour = response.data.colour;
        })
        .catch(e => {
          console.log('SHARELINK ERROR...');
        });
    },
  }
</script>

<style scoped>
* {
  font-family: 'Roboto', sans-serif;

}
  .file-header {
    text-align: center;
    margin: 20px;
    color: #fff;
    font-weight: 100;
  }

  .AudioPlayerContainer {
    margin: 0 100px;
  }
</style>
