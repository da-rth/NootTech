<template>
  <div>
    <notifications group="SettingsUpdate" />
    <b-modal
      ref="modal"
      title="Settings"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      ok-title="Save Settings"
      @ok="saveSettings"
      @hidden="resetSettings"
      >
      <h1>Settings</h1>

      <b-form>
        <b-form-group
          label="Select a new colour"
          label-for="colourSettingsField">
          <slider id="colourSettingsField" v-model="colour" />
        </b-form-group>

        <b-form-group
          class="form-inline"
          label="insert a new email"
          label-for="emailSettingsField"
          >
          <b-form-input
            id="emailSettingsField"
            v-model="settings.email"
            :placeholder="$store.state.settings.email"
            type="email"
            />
        </b-form-group>

        <b-form-group
          class="form-inline"
          label="Your upload key">
          <label for="uploadkeySettingsField">Your upload key</label><br/>
          <b-input
          id="uploadkeySettingsField"
          disabled
          :value="$store.state.settings.upload_key"
          class="form-control" />
          <b-button variant="success">Copy</b-button>
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
    computed: {
      getColour() {
        var colour = this.colour
        if(typeof (colour) !== "string")
          colour = colour.hex;
        return colour;
      }
    },
    watch: {
      colour() {
        this.$root.colour = this.getColour
      }
    },
    methods: {
      show() {
        this.$refs.modal.show()
      },
      async saveSettings() {
        try{
          this.settings.colour = this.getColour;

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
      EventBus.$on('settingsModal', () => {this.show()})
      resetSettings()
   }
}
</script>

<style scoped>
</style>
