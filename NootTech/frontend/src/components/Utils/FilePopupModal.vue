<template>
	<div :value="value" @input="$emit('input', $event.target.value)">
		<b-modal size="lg" centered :ref="modalId" :title="value.original_filename">
      <p>
      <br/>
        <img class="preview-image" v-if="value.file_mime_type.startsWith('image') && value.file_image_info.is_web_safe" :src="value.file_content"/>
        <h4>{{ value.generated_filename }}</h4>
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
			modalId: "_popup-" + this.value.id
		}
	},
	methods: {
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
</style>
