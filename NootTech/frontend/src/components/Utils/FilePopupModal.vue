<template>
	<div :value="value" @input="$emit('input', $event.target.value)">
		<b-modal size="lg" centered :ref="modalId" :title="value.original_filename">
      <p>
      <br/>
        <template v-if="value.file_image_info">
          <img
              class="preview-image"
              v-if="value.file_mime_type.startsWith('image') && value.file_image_info.is_web_safe"
              :src="value.file_content"/>
          <h2 v-else>download only, no preview</h2>
        </template>

          <b-input-group class="copy-sharelink-group">
            <b-form-input v-bind:value="getShareLink()" readonly/>
            <b-input-group-append>
              <a :href="getShareLink()"><b-button>Open</b-button></a>
              <input type="hidden" id="sharelink" :value="getShareLink()">
              <b-button>Copy</b-button>
            </b-input-group-append>
          </b-input-group>

      </p>
		</b-modal>
	</div>
</template>

<script>
export default {
	name: "NtPopupaModal",
	props: ["value"],
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

<style scoped>
  .preview-image {
    width: 100%;
    height: auto;
    border: 1px solid black;
    margin: 0 auto;
  }

  .copy-sharelink-group {
    margin: 20px 0;
  }
</style>
