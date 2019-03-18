<template>
	<div>
    <notifications group="ReportNotif" />
		<b-modal size="lg" centered scrollable ref="modal" title="Report file" @hidden="report=null" bodyBgVariant="dark" headerBgVariant="dark" footerBgVariant="dark" :ok-disabled="selected == null || text == ''"
      ok-title="Report File"
      @ok="reportFile">
      
      <b-form-select v-model="selected" :options="options" class="mb-3" required>
        <template slot="first">
          <option :value="null" disabled>-- Please select an option --</option>
        </template>
      </b-form-select>

        <b-form-textarea
          id="textarea-rows"
          placeholder="Please give more information about your report."
          rows="10"
          v-model="text"
          required
        />
    </b-modal>
	</div>
</template>

<script>
import EventBus from '../../event-bus.js';

export default {
	name: "NtReportFileModal",
	data() {
		return {
      text: '',
      selected: null,
      options: [
          { text: 'Infringes my copyright' },
          { text: 'Infringes my rights' },
          { text: 'Malicious or virus' },
          { text: 'Spam or misleading' },
          { text: 'Hateful or abusive' },
          { text: 'Child abuse' },
          { text: 'Other reason' },
        ]
		}
  },
  props: ['file'],
  
  mounted() {
    var that = this;
    EventBus.$on("reportPopup", file => {
      that.file = file;
      that.showModal();
    });
  },

	methods: {
		// wrappers
		showModal () {
			this.$refs.modal.show();
		},
		hideModal () {
      this.$refs.modal.hide();
    },
    async reportFile() {
      console.log("Submitting report for:");
      let report = {
        reason_title: this.selected,
        reason_body: this.text,
        // If user isn't authenticated, send report with user ID which will be a pre-created user called "Anonymous"
        reported_by: this.$store.state.user != null ? this.$store.state.user.user_id : 1,
        reported_file: this.file.id
      }
      await this.$api.ReportFile(report)
      .then(response => {
          console.log("REPORT SUCCESS", response);
          this.$notify({
            group: 'ReportNotif',
            title: 'Success: Thank you for submitting your report!',
            text: 'Our administrators will look into it for you.',
          });
      }).catch(e => {
          console.log('REPORT ERROR...', e);
          this.$notify({
            group: 'ReportNotif',
            title: 'Whoops, we had some trouble submitting your report...',
            text: 'Please try again later. Your reports are important to us.',
          });
      });;
    }
  }
}
</script>
