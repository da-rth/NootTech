<template>
    <b-modal
      id="uploadFileModal"
      ref="modal"
      title="File Upload"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      header-border-variant="dark"
      footer-border-variant="dark"
      :ok-disabled='upload_data.files.length == 0'
      ok-title="Upload file(s)"
      scrollable
      @ok="uploadFiles"
      @hidden="clearFiles"
      >
      <h4>You can select one or more files.</h4>
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
          <b-button class="upload-modal-btn" @click="upload_data.is_private = !upload_data.is_private">
          <font-awesome-icon icon="lock" v-if="upload_data.is_private"/>
          <font-awesome-icon icon="lock-open" v-else/>
          {{ upload_data.is_private ? "Send as private" : "Send as public"}}
          </b-button>
          <div v-if="upload_data.files.length > 0">
            <b-button @click="clearFiles" class="upload-modal-btn">Clear selected files</b-button>
            <br/>
            <div class="selected-files">
            You have selected:
            <ul>
              <li :key="file.id" v-for="file in upload_data.files">{{ file.name }}</li>
            </ul>
            </div>
          </div>
        </b-form-group>
      </b-form>
    </b-modal>
</template>

<script>

export default {
  name: 'NtUploadModal',

  methods: {
   clearFiles() {
      this.upload_data.is_private = false;
      this.upload_data.files = new Array();
    },
    async uploadFiles() {
      console.log("Trying to upload " + this.upload_data.files);

      await this.$api.UploadFiles(this.upload_data)
      .then(response => {
        console.log('Successful server response:', response);
        this.$notify({
          group: 'Global',
          title: `Successfully uploaded file(s)!`,
          text: 'The file panel is now updating...',
          position: 'bottom right'
        });
        this.$root.$emit('refreshFilePanel');
      })
      .catch(e => {
        // Catch the error and notify user that file cant be deleted
        console.log('ERROR', e.response);
        console.log("Could not upload the file...")
        this.$notify({
          group: 'Global',
          title: `Could not uploaded file(s)`,
          text: 'Something went wrong on our end...',
          position: 'bottom right'
        });
        return null
      });
   },
  },
  data() {
    return {
      upload_data: {
        username: '',
        upload_key: '',
        is_private: false,
        files: [],
        }
    };
  },
  mounted() {
    this.upload_data.username = this.$store.state.user.username;
    this.upload_data.upload_key = this.$store.state.settings.upload_key;
 }
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

.upload-modal-btn {
  width: 100%;
  background-color: #202020 !important;
  margin: 5px 0px;
}

.selected-files {
  background-color: rgba(0,0,0,0.2);
  padding: 10px;
}
</style>
