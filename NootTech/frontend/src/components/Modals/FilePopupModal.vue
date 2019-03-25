<template>
	<div>
		<b-modal
      id="filePopupModal"
      size="lg"
      centered
      scrollable
      ref="modal"
      :title="getTitle"
      @hidden="file=null"
      bodyBgVariant="dark"
      headerBgVariant="dark"
      footerBgVariant="dark"
      header-border-variant="dark"
      footer-border-variant="dark"
      >

      <template v-if="file">
        <VideoPlayer :file="file" v-if="file.file_video_info" class="fo-container"/>
        <AudioPlayer :file="file" v-else-if="file.file_audio_info" class="fo-container"/>
        <ImagePreview :file="file" v-else-if="file.file_image_info" class="fo-container img"/>
        <TextPreview :file="file" v-else-if="file.file_text_info" class="fo-container"/>
        <div class="popup-file-icon" v-else>
          <font-awesome-icon :icon="getIcon(file)"/>
        </div>
        
        <b-button v-b-toggle.collapseA.collapseB class="file-info-btn">Toggle File Information</b-button>
        <b-collapse id="collapseA" class="mt-2">
          <b-card><FileInformation :file="file"/></b-card>
        </b-collapse>

        <nt-file-settings :file="file"/>
        
        <b-input-group prepend="Sharelink:" class="copy-sharelink-group" v-if="!file.is_private">
          
          <b-form-input :value="getShareLink()" readonly/>
          <b-input-group-append>
            <a :href="getShareLink()"><b-button class="copy-open-btn"><font-awesome-icon icon="link"/></b-button></a>
            <input type="hidden" id="sharelink" :value="getShareLink()">
          </b-input-group-append>
          <b-input-group-append>
            <b-button @click="copySharelink" class="copy-open-btn"><font-awesome-icon icon="copy"/></b-button>
          </b-input-group-append>
        </b-input-group>

        
      </template>
    </b-modal>
	</div>
</template>
<script>

  import VideoPlayer from "../Utils/FilePreview/VideoPlayer.vue";
  import AudioPlayer from "../Utils/FilePreview/AudioPlayer";
  import DownloadFile from "../Utils/FilePreview/DownloadFile";
  import ImagePreview from "../Utils/FilePreview/ImagePreview";
  import TextPreview from "../Utils/FilePreview/TextPreview.vue";
  import FileInformation from "../Utils/FilePreview/FileInformation";
  import NtFileSettings from '../Utils/FileSettings.vue';

export default {
	name: "NtFilePopupModal",
  components: {
      TextPreview,
      ImagePreview,
      DownloadFile,
      AudioPlayer,
      VideoPlayer,
      FileInformation,
      NtFileSettings
    },
	data() {
		return {
      file: null
		}
	},
	methods: {
    getIcon(file) {
        // split into prefix and second name
        let src_icon = file.icon.split(" ")
        // it seems fontawesome is not happy with the fa-prefix
        src_icon[1] = src_icon[1].replace(/^fa-/gi, "");
        return src_icon
      },
    getShareLink () {
      let username = this.$store.state.user.username;
      if (this.$subdomain_enabled) {
        return `${this.$site_url.replace("//","//"+username+".")}/${this.file.generated_filename}`
      } else {
        return `${this.$site_url}/u/${username}/${this.file.generated_filename}`
      }
    },
    copySharelink () {
      let testingCodeToCopy = document.querySelector('#sharelink')
      testingCodeToCopy.setAttribute('type', 'text')
      testingCodeToCopy.select()
      try {
        var successful = document.execCommand('copy');
        this.showUploadKey = false;
        this.$notify({
          group: 'Global',
          title: `Copied the URL to clipboard!`,
          text: 'Go ahead! Paste it like crazy!',
        });
      } catch (err) {
        this.$notify({
          group: 'Global',
          title: 'Oh no! We couldn\'t copy the URL',
          text: 'Try using CTRL+C! Sorry about that...',
        });
      }
      testingCodeToCopy.setAttribute('type', 'hidden')
      window.getSelection().removeAllRanges()
  },
  },
  mounted() {
    this.$root.$on("filePopupModal", file => {
      this.file = file;
      this.$refs.modal.show();
    });
  },
  computed: {
    getTitle() { return this.file ? this.file.original_filename : ""; }
  }
}
</script>

<style scoped>
#NTImage {
  max-height: 400px;
}
</style>

<style>
  .preview-image {
    width: 100%;
    height: auto;
    border: 1px solid black;
    margin: 0 auto;
  }

  .copy-sharelink-group {
      margin: 10px auto;
      width: 60%;
  }

  .modal-content {
    color: white;
    background-color: #242424;
  }

  .fo-container {
    max-height: 40vh;
  }

  #NTImage {
    margin: 0 auto;
    max-width: 90%;
  }

  #collapseA .card {
    background: transparent;
  }

  #FileInformation {
    margin-bottom: 10px !important;
  }

  .hljs {
    text-align: left !important;
    margin: 0 !important;
    min-height: 50% !important;
  }

  .file-info-btn {
    margin: 10px;
    width: 100%;
    background: transparent !important;
    border: none !important;
    color: rgba(255,255,255,0.8) !important;
    transition: color 0.5s ease-in-out;
  }

  .file-info-btn:hover {
    color: rgba(255,255,255, 1) !important;
  }

  .file-info-btn:focus {
    box-shadow: none !important;
  }

  .popup-file-icon {
    background: #202020;
    text-align: center;
    font-size: 140px;
    border: 1px solid black;
  }

  .copy-open-btn {
    border-radius: 0px !important;
    background: #e9ecef !important;
    border-color: #d1d6dc !important;
  }

  .input-group-text {
    margin-bottom: 1.5px !important;
  }
</style>
