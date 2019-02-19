<template>
	<div :value="value" @input="$emit('input', $event.target.value)">
		<b-modal :ref="modalId" title="Image settings">

		</b-modal>
	</div>
</template>
<script>
export default {
	name: "NtImageBadge",
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
