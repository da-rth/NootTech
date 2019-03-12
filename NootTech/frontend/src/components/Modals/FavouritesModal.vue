<template>
    <b-modal
      ref="modal"
      title="Favourited Files"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      >
      <h1>Favourites</h1>
      {{ JSON.stringify(favourites) }}
      <!-- 
        Have a v-for here showing all favourites
        Each fav will have an X button. When clicked, deleteFavourite() is called. If successful, pop favourite from favourites.
       -->
    </b-modal>
</template>

<script>
export default {
    name: 'NtFavouritesModal',

    methods: {
      show() {
        this.$refs.modal.show()
      },
      async deleteFavourite(fileID) {
        await this.$api.deleteFavourite(fileID)
          .then(response => {
            favourites_deleted++;
            console.log('FAVOURITES DELETION SUCCESS:', response);
            // remove favourite from favourites.
            this.$notify({
              group: 'FavouritesUpdate',
              title: `Successfully removed from favourites!`,
              position: 'bottom right'
            });
          })
          .catch(e => {
            console.log('ERROR', e.response);
          });
      },
    },
    data() {
      return {
        favourites: this.$store.state.favourites
      };
    },
}
</script>

<style scoped>
</style>
