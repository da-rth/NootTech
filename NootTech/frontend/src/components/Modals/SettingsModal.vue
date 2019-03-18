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
      
      <b-form-group
        label="select a new colour"
        label-for="colourSettingsField">
        <slider id="colourSettingsField" v-model="settings.colour" />
      </b-form-group>

      <b-form-group
        label="insert a new email"
        label-for="emailSettingsField"
        >
        <b-form-input id="emailSettingsField" v-model="settings.email" type="email" required/>
      </b-form-group>

      <br/>
      {{ settings.upload_key }}
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
        var colour = this.settings.colour;
        if(typeof (colour) !== "string")
          colour = colour.hex;
        return colour;
      }
    },
    methods: {
      show() {
        this.$refs.modal.show()
      },
      async saveSettings() {
        try{
          this.settings.colour = this.getColour;
          console.log(this.settings);
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
        this.settings.email = this.original.email;
        this.settings.colour = this.$root.colour = this.original.colour;

      }
    },
    data() {
      return {
        settings: {
          email: this.$store.state.settings.email,
          colour: this.$root.colour,
          upload_key: this.$store.state.settings.upload_key
        },
        original: {}
      };
    },
    mounted() {
      EventBus.$on('settingsModal', () => {this.show()})
      this.original = {
        email: this.$store.state.settings.email,
        colour: this.$root.colour,
        upload_key: this.$store.state.settings.upload_key
      }
    }
}
</script>

<style scoped>
</style>
