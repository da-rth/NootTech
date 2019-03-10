<template>
  <div>
    <LoadingFiles :multiple="true" v-if="isLoading"></LoadingFiles>
    <template v-else>
      <FilePanel></FilePanel>
    </template>
  </div>
</template>

<script>
  import LoadingFiles from '../FilePanel/LoadingFiles';
  import FilePanel from '../FilePanel/Panel';
  import EventBus from '../../event-bus.js'

  export default {
    name: "AuthenticatedPane",
    data () {
      return {
        gsize: null,
        files: null,
        searched_files: null,
        filesToDelete: [],
        isLoading: true
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
        })
        .finally(() => {
          this.isLoading = false;
          this.$root.shareLinkName = null;
          this.$root.colour = this.$store.state.settings.colour;
        })
      },
   },
    created() {
      EventBus.$on('refreshFilePanel', this.loadFiles);
    },
    mounted() {
      // it is safe to emit after mouting everything
      EventBus.$emit('refreshFilePanel');
    }
 }
</script>

<style scoped>

</style>
