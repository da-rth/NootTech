<template>
  <div>
    <LoadingFiles :multiple="true" v-if="isLoading"></LoadingFiles>
    <template v-else>
      <!--FileMenu></ileMenu-->
      <FilePanel></FilePanel>
    </template>
  </div>
</template>

<script>
  import LoadingFiles from '../FilePanel/LoadingFiles';
  import FilePanel from '../FilePanel/Panel';
  export default {
    name: "AuthenticatedPane",
    data () {
      return {
        gsize: null,
        files: null,
        searched_files: null,
        settings: null,
        isLoading: false,
        filesToDelete: []
      }
    },
    components: {
      FilePanel,
      LoadingFiles,
    },

    methods: {

      async loadFiles() {
        await this.$api.GetFiles()
        .then(response => {
          console.log('GET FILES SUCCESS', response);
          this.files = response.data;
          this.searched_files = response.data;
          this.isLoading = false;
        })
        .catch(e => {
          console.log('GET FILES ERROR', e.response);
          this.isLoading = false;
        });
      },

      async loadSettings() {
        await this.$api.GetSettings()
        .then(response => {
          console.log('SETTINGS SUCCESS', response);
          this.settings = response.data;
        })
        .catch(e => {
          console.log('SETTINGS ERROR', e.response);
        });
      },

    },
    async beforeMount () {
        this.isLoading = true;
        await this.loadSettings();
        await this.loadFiles();
    },
  }
</script>

<style scoped>

</style>
