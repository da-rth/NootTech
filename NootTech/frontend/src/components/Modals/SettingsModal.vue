<template>
    <b-modal
      ref="modal"
      title="Settings"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      :ok-disabled='modified_setting_fields == 0'
      ok-title="Save Settings"
      @ok="uploadFiles"
      @cancel="clearFiles"
      >
      <h1>Settings</h1>
      You can select one or more files.
      <br/>
      {{ colour }}
      <br/>
      {{ upload_key }}
      <br/>
      {{ email }}
    </b-modal>
</template>

<script>
export default {
    name: 'NtSettingsModal',

    methods: {
      show() {
        this.$refs.modal.show()
      },
      async saveSettings() {
        await this.$api.UpdateSettings(this.settings)
        .then(response => {
          console.log('SETTINGS UPDATE SUCCESS:', response);
          this.$notify({
            group: 'SettingsUpdate',
            title: `Successfully updated settings!`,
            position: 'bottom right'
          });
        })
        .catch(e => {
          // Catch the error and notify user that file cant be deleted
          console.log('ERROR', e.response);
          console.log("Could not upload the file...")
          return null
        });
      },
    },
    data() {
      return {
        modified_setting_fields: 0,
        settings: {
          email: this.$store.state.settings.email,
          colour: this.$store.state.settings.colour,
          upload_key: this.$store.state.settings.upload_key
        }
      };
    },
}
</script>

<style scoped>
</style>
