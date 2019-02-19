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
      async getData() {
        this.isLoading = true;
        this.settings = await this.$api.GetSettings();
        this.files = await this.$api.GetFiles();
        this.searched_files = this.files;
        this.isLoading = false;
      }
    },
    beforeMount () {
      this.getData()
    },
  }
</script>

<style scoped>

</style>
