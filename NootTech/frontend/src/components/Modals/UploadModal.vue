<template>
    <b-modal
      ref="modal"
      title="Upload"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      :ok-disabled='upload_data.files.length == 0'
      ok-title="Upload file(s)"
      @ok="uploadFiles"
      @cancel="clearFiles"
      >
      <h1>File upload</h1>
      You can select one or more files.

      <b-form class="upload-form">
        <b-form-group>
          <b-form-file
            v-model="upload_data.files"
            class="file-selection-area"
            :state="upload_data.files.length > 0"
            placeholder="Choose one or more file..."
            drop-placeholder="Drop one or more files here..."
            browse-text="Select file(s)"
            multiple
          />
          <div class="mt-3" v-if="upload_data.files.length > 0">
            <b-button @click="clearFiles" class="mr-2">Clear selected files</b-button>
            <br/>
            You have selected:
            <ul>
              <li :key="file.id" v-for="file in upload_data.files">{{ file.name }}</li>
            </ul>
          </div>
        </b-form-group>

        <b-button class="set-private-btn" @click="upload_data.is_private = !upload_data.is_private">
          <font-awesome-icon icon="lock" v-if="upload_data.is_private"/>
          <font-awesome-icon icon="lock-open" v-else/>
          Set Private: {{ upload_data.is_private }}
        </b-button>
      </b-form>
    </b-modal>
</template>

<script>
export default {
    name: 'NtUploadModal',

    methods: {
      show() {
        this.$refs.modal.show()
      },
      clearFiles() {
        this.upload_data.files.length = 0
      },
      async uploadFiles() {
        await this.$api.UploadFiles(this.upload_data)
        .then(response => {
          console.log('Successful server response:', response);
          this.$notify({
            group: 'FileUpload',
            title: `Successfully uploaded file(s)!`,
            text: 'The file panel is now updating...',
            position: 'bottom right'
          });
          this.$store.commit('REFRESH_FILE_PANEL', true);

        })
        .catch(e => {
          // Catch the error and notify user that file cant be deleted
          console.log('ERROR', e.response);
          console.log("Could not upload the file...")
          return null
        });
        /**
         * TODO: implement an Observer with LoadingFiles (or just use a watch with some global vars)
         */
      },
    },
    data() {
      return {
        upload_data: {
          username: this.$store.state.user != null ? this.$store.state.user.username : "",
          upload_key: this.$store.state.settings != null ? this.$store.state.settings.upload_key : "",
          is_private: false,
          files: [],
          }
      };
    },
}
</script>

<style scoped>
.privacy-switch {
  text-align: center;
  margin: 0 auto;
  padding: 5px;
}

.upload-form {
  margin: 30px 0;
}

.file-selection-area {
    overflow-y: hidden;
    height: 35px;
    border-radius: 5px;
}
</style>
