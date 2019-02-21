<template>
  <div class="justify-content-center">
    <template v-if="file">
      <h2 class="file-header">{{ this.file.original_filename }}</h2>
      <VideoPlayer :file="file" v-if="file.file_video_info"/>
      <AudioPlayer :file="file" v-else-if="file.file_audio_info"/>
      <ImagePreview :file="file" v-else-if="file.file_image_info"/>
      <TextPreview :file="file" v-else-if="file.file_text_info"/>
      <DownloadFile :file="file" />
      <VirusTotal :file="file" v-if="file.virus_scan"/>
    </template>
  </div>
</template>

<script>
  import LoadingFiles from '../FilePanel/LoadingFiles';
  import FilePanel from '../FilePanel/Panel';
  import VideoPlayer from "../Utils/FilePreview/VideoPlayer";
  import AudioPlayer from "../Utils/FilePreview/AudioPlayer";
  import DownloadFile from "../Utils/FilePreview/DownloadFile";
  import VirusTotal from "../Utils/FilePreview/VirusTotal";
  import ImagePreview from "../Utils/FilePreview/ImagePreview";
  import TextPreview from "../Utils/FilePreview/TextPreview";


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
      VirusTotal,
      DownloadFile,
      AudioPlayer,
      VideoPlayer,
      FilePanel,
      LoadingFiles,
    },

    async created () {
        this.username = this.$route.params.username;
        this.gen_name = this.$route.params.gen_name;
        let data = await this.$api.GetShareData(this.username, this.gen_name);
        this.file = data.file;
        this.colour = data.colour;
        console.log("DATA", this.data)
    },
  }
</script>

<style scoped>
* {
  font-family: 'Roboto', sans-serif;

}
  .file-header {
    text-align: center;
    margin: 30px 0 15px 0;
    color: #00cccc;
    font-weight: 100;
  }
</style>
