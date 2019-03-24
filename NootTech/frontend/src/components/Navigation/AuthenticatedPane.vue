<template>
  <div>
    <notifications group="FileLoading"/>
    <LoadingFiles :multiple="true" v-if="isLoading"></LoadingFiles>
    <template v-else>
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
        isLoading: true
      }
    },
    components: {
      FilePanel,
      LoadingFiles,
    },
    methods: {
      async loadFavourites() {
        try {
          let response = await this.$api.GetFavourites();
          this.$root.favourite_files = response.data;
        } catch(e) {
          this.$notify({
            group: 'FileLoading',
            type: "error",
            title: `Couldn't fetch favourites!`
          })
          console.log('GET FAVOURITE ERROR', e);
        }
      },
      async loadFiles() {
        this.isLoading = true;
        await this.$api.GetFiles()
        .then(response => {
          this.$root.files = response.data;
          this.$root.searched_files = response.data;
          this.loadFavourites();
        })
        .catch(e => {
          console.log('GET FILES ERROR', e);
        })
        .finally(() => {
          this.isLoading = false;
          this.$root.shareLinkName = null;
          this.$root.colour = this.$store.state.settings.colour;
        })
      },
    },
    created() {
      this.$root.$on('refreshFilePanel', this.loadFiles);
      this.$root.$on('refreshFavourites', this.loadFavourites);
    },
    mounted() {
      this.loadFiles();
    }
 }
</script>

<style scoped>

</style>
