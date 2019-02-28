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
        this.isLoading = true;
        await this.$api.GetFiles()
        .then(response => {
          console.log('GET FILES SUCCESS', response);
          this.files = response.data;
          this.searched_files = response.data;
        })
        .catch(e => {
          console.log('GET FILES ERROR', e.response);
        });
        this.isLoading = false;
      },

      changeColour() {
        if (this.$store.state.settings) {
          this.$root.colour = this.$store.state.settings.colour;
        }
      }
    },

    async mounted() {
      await this.loadFiles();
      this.changeColour();
      this.$root.sharelinkName = null;
    }
  }
</script>

<style scoped>

</style>
