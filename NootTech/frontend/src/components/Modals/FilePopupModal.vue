<template>
	<div :value="value" @input="$emit('input', $event.target.value)">
		<b-modal size="lg" centered scrollable :ref="modalId" :title="value.original_filename">

    <template v-if="value">

      <VideoPlayer :file="value" v-if="value.file_video_info" class="fo-container"/>
      <AudioPlayer :file="value" v-else-if="value.file_audio_info" class="fo-container"/>
      <ImagePreview :file="value" v-else-if="value.file_image_info" class="fo-container img"/>
      <TextPreview :file="value" v-else-if="value.file_text_info" class="fo-container"/>
      
      <br/>
      
      <b-button v-b-toggle.collapseA.collapseB>Toggle File Information</b-button>
      
      <b-collapse id="collapseA" class="mt-2">
        <b-card><FileInformation :file="value"/></b-card>
      </b-collapse>

    </template>

    <b-input-group class="copy-sharelink-group">
        <b-form-input v-bind:value="getShareLink()" readonly/>
        <b-input-group-append>
          <a :href="getShareLink()"><b-button>Open</b-button></a>
          <input type="hidden" id="sharelink" :value="getShareLink()">
          <b-button>Copy</b-button>
        </b-input-group-append>
      </b-input-group>
		</b-modal>

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
	name: "NtPopupaModal",
  props: ["value"],
  components: {
      TextPreview,
      ImagePreview,
      DownloadFile,
      AudioPlayer,
      VideoPlayer,
      FileInformation
    },
	data() {
		return {
      modalId: "_popup-" + this.value.id,
		}
	},
	methods: {
    getShareLink () {
      let username = this.$store.state.user.username;
      if (this.$subdomain_enabled) {
        return `${this.$site_url.replace("//","//"+username+".")}/${this.value.generated_filename}`
      } else {
        return `${this.$site_url}/u/${username}/${this.value.generated_filename}`
      }
    },
		// wrappers
		showModal () {
			this.$refs[this.modalId].show();
		},
		hideModal () {
			this.$refs[this.modalId].hide();
		}
	},
}
</script>

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
    max-height: 50%;
  }

  #collapseA .card {
    background: transparent;
    min-height: 20vw;
  }

  #FileInformation {
    margin-bottom: 10px !important;
  }

  .hljs {
    text-align: left !important;
  }
</style>
