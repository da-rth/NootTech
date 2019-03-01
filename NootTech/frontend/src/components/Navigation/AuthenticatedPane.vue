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
        filesToDelete: []
      }
    },
    components: {
      FilePanel,
      LoadingFiles,
    },
    computed: {
      isLoading() {
        return this.$store.state.refresh_file_panel;
      }
    },
    watch: {
      async isLoading(newValue, oldValue) {
        if (newValue)
          await this.loadFiles();
      }
    },

    methods: {
      async loadFiles() {
        await this.$api.GetFiles()
        .then(response => {
          console.log('GET FILES SUCCESS', response);
          this.files = response.data;
          this.searched_files = response.data;
        })
        .catch(e => {
          console.log('GET FILES ERROR', e.response);
        })
        .finally(() => {
          this.$store.commit('REFRESH_FILE_PANEL', false); 
        })
      },

    },
    async beforeMount () {
        this.sharelinkColour = null;
        if(!this.$store.state.refresh_file_panel)
          this.$store.commit('REFRESH_FILE_PANEL', true);
        await this.loadFiles();
    },
  }
</script>

<style scoped>

</style>
