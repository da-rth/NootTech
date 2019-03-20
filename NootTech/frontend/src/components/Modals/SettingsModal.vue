<template>
  <div>
    <notifications group="SettingsUpdate" />
    <b-modal
      ref="modal"
      title="Settings"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      header-border-variant="dark"
      footer-border-variant="dark"

      ok-title="Save Settings"
      @ok="saveSettings"
      @hidden="resetSettings"
      centered
      >

      <b-form>
        <b-form-group
          class="col-lg-12"
          label="Pick a new colour"
          label-for="colourSettingsField">
          <b-input-group>
            <slider id="colourSettingsField" v-model="colour" />
          </b-input-group>
        </b-form-group>

        <b-form-group
          class="col-lg-12"
          label="Your email"
          label-for="emailSettingsField"
          >
          <b-input-group>

            <b-input
              id="emailSettingsField"
              v-model="settings.email"
              :placeholder="$store.state.settings.email"
              type="email"/>
          </b-input-group>
        </b-form-group>

        <b-form-group
          class="col-lg-12"
          label="Your upload key"
          label-for="uploadkeySettingsField">
          <b-input-group>
            <b-input
            id="uploadkeySettingsField"
            disabled
            :value="$store.state.settings.upload_key"
            class="form-control" />
            <b-button variant="success" @click="copyUploadKey">Copy</b-button>
          </b-input-group>
        </b-form-group>

        <b-form-group
          class="col-lg-12"
          label="Click the button below to delete your account.">
        <b-button>Delete Account</b-button>
        
        </b-form-group>

      </b-form>
    </b-modal>
  </div>
</template>

<script>
import EventBus from '../../event-bus.js';
import {Slider} from 'vue-color';
import {SETTINGS} from '../../store/mutation-types.js'

export default {
    name: 'NtSettingsModal',
    components: { Slider },
    watch: {
      colour(newValue) {
          if(newValue != null && typeof(newValue) !== "string") {
            console.log(newValue)
            this.$root.colour = newValue.hex;
          }
      }
    },
    methods: {
      show() {
        this.$refs.modal.show()
      },
      copyUploadKey() {
        let testingCodeToCopy = document.querySelector("#uploadkeySettingsField")
        testingCodeToCopy.removeAttribute("disabled")
        testingCodeToCopy.select()
        
        try {
          var successful = document.execCommand('copy');
          console.log(successful)
          this.$notify({
            group: 'SettingsUpdate',
            title: `Copied the key to clipboard!`,
            text: 'Go ahead! Paste it like crazy!',
          });
        } catch (err) {
          this.$notify({
            group: 'SettingsUpdate',
            title: 'Oh no! We couldn\'t copy the key',
            text: 'Sorry about that...',
          });
        }
        testingCodeToCopy.setAttribute("disabled", "disabled")
      },
	
      async saveSettings() {
        try{
          this.settings.colour = this.$root.colour;

          // avoid filling a null entry
          if(this.settings.email == "")
            delete this.settings.email;

          let response = await this.$api.UpdateSettings(this.settings)
          console.log('SETTINGS UPDATE SUCCESS:', response);
          this.$notify({
            group: 'SettingsUpdate',
            title: `Successfully updated settings!`,
            position: 'bottom right'})
          this.$store.dispatch(SETTINGS);
        }
        catch(e) {
          // Catch the error and notify user that file cant be deleted
          console.log('ERROR', e);
          console.log("Could not change the settings...")
        }
      },
      resetSettings() {
        this.settings.colour = this.colour = this.$root.colour = this.$store.state.colour;
      }
    },
    data() {
      return {
        settings: {
          email: "",
          colour: ""
        },
        colour: this.$root.colour
      };
    },
    mounted() {
      EventBus.$on('settingsModal', () => {
        if(this.$refs.modal)
          this.show()
      });
      this.resetSettings();
   }
}
</script>

<style scoped>
</style>
