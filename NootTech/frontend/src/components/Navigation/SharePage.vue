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

      <ReportFileModal :file="file"/>

      <div v-if="this.$store.state.user && this.$store.state.user.username != this.username" class="report-btn-container">
        <b-button class="report-btn" @click="onClick"><font-awesome-icon icon="flag"/>&nbsp; Report this file</b-button>
      </div>
    </template>

    <div v-else class="private-container">
      <h1 class="private-msg">File is set to private or does not exist.</h1>
      <font-awesome-icon icon="sad-cry" class="big-sad" />
    </div>
  </div>
</template>

<script>
  import EventBus from '../../event-bus.js';
  import VideoPlayer from "../Utils/FilePreview/VideoPlayer";
  import AudioPlayer from "../Utils/FilePreview/AudioPlayer";
  import DownloadFile from "../Utils/FilePreview/DownloadFile";
  import ImagePreview from "../Utils/FilePreview/ImagePreview";
  import TextPreview from "../Utils/FilePreview/TextPreview";
  import FileInformation from "../Utils/FilePreview/FileInformation";
  import ReportFileModal from "../Modals/ReportFileModal";

  import router from '../../router/index.js';

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
      FileInformation,
      ReportFileModal
    },

    methods: {
      onClick () {
        console.log("test");
        EventBus.$emit('reportPopup', this.file);
      }
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
          console.log(e.response.data);
          console.log('SHARELINK ERROR...');
          router.push('/404');
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
  .report-btn-container {
    padding: 40px;
  }

  .report-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #202020;
    border: 1px solid #3d3d3d;
  }

  .report-btn:hover {
    background-color: transparent;
    border-color: #FF0000;
    opacity: 0.9;
  }

  .private-container {
    padding: 50px;
    text-align: center;
  }

  .big-sad {
    margin: 20px;
    font-size: 150px;
  }
</style>
