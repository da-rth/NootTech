<template>
  <div>
    
    <b-modal
      id="settingsModal"
      title="Settings"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      header-border-variant="dark"
      footer-border-variant="dark"

      ok-title="Save Settings"
      @ok="saveSettings"
      @cancel="resetSettings"
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
          class="col-lg-12 form-inline">
          <b-button variant="warning" v-b-modal.showPasswordModal>Change password</b-button>
          <b-button variant="danger" v-b-modal.showDeleteModal>Delete account</b-button>
        </b-form-group>
      </b-form>
    </b-modal>
    <b-modal id="showPasswordModal"
      ref="changePasswordModal"
      title="Change password"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      header-border-variant="dark"
      footer-border-variant="dark"
      ok-variant="danger"
      @ok="changePassword"
      @cancel="password.newPassword = password.oldPassword = ''"
      >
      <b-form-group
        label="Please provide your current password"
        label-for="oldPasswordField"
      >
      <b-input
        id="oldPasswordField"
        type="password"
        v-model="password.oldPassword"
        autocomplete="off"
        required
        >
      </b-input>
      </b-form-group>
      <b-form-group
        label="Please provide a new password"
        label-for="newPasswordField"
      >
      <b-input
        id="newPasswordField"
        type="password"
        v-model="password.newPassword"
        required
        autocomplete="new-password"
        :state="password.newPassword != password.oldPassword">
      </b-input>
      </b-form-group>
    </b-modal>
    <b-modal
      id="showDeleteModal"
      ref="DeleteUserModal"
      title="Delete account"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      header-border-variant="dark"
      footer-border-variant="dark"
      ok-variant="danger"
      ok-title="I understand the risk, delete me!"
      @ok="deleteAccount"
      >
      <b-form-group
        label="Please insert your password"
        label-for="password">
        <b-input
          id="passwordDeleteField"
          type="password"
          v-model="password.oldPassword"
          autocomplete="off"
          required
          />
      </b-form-group>
    </b-modal>
  </div>
</template>

<script>
import {Slider} from 'vue-color';
import {SETTINGS} from '../../store/mutation-types.js'

export default {
  name: 'NtSettingsModal',
  components: { Slider },
  data() {
    return {
      settings: {
        email: "",
        colour: ""
      },
      password: {
        oldPassword: "",
        newPassword: "",
      },
      colour: this.$root.colour
    };
  },
  watch: {
    colour(newValue) {
        if(newValue == null) return;
        if(typeof(newValue) !== "string") {
          this.$root.colour = newValue.hex;
        }
        else this.$root.colour = newValue;
    }
  },
  methods: {
   async changePassword(evt) {
      // avoid closing the modal
      evt.preventDefault();
      try {
        await this.$api.ChangePassword(this.password.oldPassword, this.password.newPassword);
        this.$notify({
          group: 'Global',
          title: `Password changed successfully`,
        });
        this.$refs.changePasswordModal.hide();
      } catch(e) {
        console.log("CHANGE PASSWORD ERROR", e);
          this.$notify({
          group: 'Global',
          type: "error",
          duration: -1,
          title: `Couldn't change the password`,
          text: typeof(e.response.data.detail) === "string" ?
                        e.response.data.detail : e.response.data.detail.join("<br>"),
        });
      }
      finally {
        this.password.oldPassword = this.password.newPassword = ""
      }
    },
    async deleteAccount(evt) {
      // avoid closing the modal
      evt.preventDefault();
      try {
        await this.$api.DeleteAccount(this.password.oldPassword);
        this.$notify({
          group: 'Global',
          title: "The user has been deleted! Unauthenticating...",
        });
        this.$router.push('/logout');
      } catch(e) {
        console.log("DELETE ACCOUNT ERROR", e);
        this.$notify({
          group: 'Global',
          type: "error",
          duration: -1,
          title: "Couldn't delete the user",
          text: e.response.data.detail
        })
      }

    },
    copyUploadKey() {
      let testingCodeToCopy = document.querySelector("#uploadkeySettingsField")
      testingCodeToCopy.removeAttribute("disabled")
      testingCodeToCopy.select()
      
      try {
        var successful = document.execCommand('copy');
        this.$notify({
          group: 'Global',
          title: `Copied the key to clipboard!`,
          text: 'Go ahead! Paste it like crazy!',
        });
      } catch (err) {
        this.$notify({
          group: 'Global',
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
        this.$notify({
          group: 'Global',
          title: `Successfully updated settings!`,
          position: 'bottom right'})
        this.$store.dispatch(SETTINGS);
      }
      catch(e) {
        // Catch the error and notify user that file cant be deleted
        console.log('ERROR', e.response.data);
        console.log("Could not change the settings...")
      }
    },
    resetSettings() {
      this.settings.colour = this.colour = this.$root.colour = this.$store.state.settings.colour;
    }
  },
  mounted() {
    this.resetSettings();
  }
}
</script>
<style>
.vc-slider-swatch:last-child {
  opacity: 0;
  display: none !important;
}
</style>
<style scoped>
</style>
