<template>
    <b-modal
      ref="modal"
      title="Favourited Files"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      @shown="loadFavourites"
      size="lg"
      scrollable
      >
      <h3 v-if="favourites.length == 0">You currently have no favourites.</h3>
      <b-card v-for="fav in favourites" no-body class="overflow-hidden fav-card" style="background-color: #242424; margin: 5px;">
        
        <b-row no-gutters>

          <b-col md="3">
            <div class="img-container-background">
              <div class="img-container">
                <img v-if="fav.thumbnail" :src="$backend_url+'/media/'+fav.thumbnail" class="img-responsive">
                <font-awesome-icon v-else :icon="getIcon(fav.icon)" style="font-size: 120px; padding: 10px;"/>
              </div>
            </div>
          </b-col>
          
          <b-col md="9">
            <b-card-body :title="fav.original">
              <b-card-text>
                Generated Filename: {{ fav.gen }}<br/>
                Uploaded by: {{ fav.username }}<br/>
                File extension: {{ fav.ext }}
              </b-card-text>
            </b-card-body>

            <div class="fav-options">
              <b-row>
                <b-button class="delete-fav-btn" v-on:click="deleteFavourite(fav.id)"> <font-awesome-icon icon="trash-alt"/> </b-button>
              </b-row>
              <b-row>
                <b-button class="copy-fav-btn"> <font-awesome-icon icon="external-link-alt"/> </b-button>
              </b-row>
              <b-row>
                <b-button class="open-fav-btn"> <font-awesome-icon icon="copy"/> </b-button>
              </b-row>
            </div>

          </b-col>
        </b-row>
      </b-card>

    </b-modal>
</template>

<script>

import EventBus from "../../event-bus.js";

export default {
    name: 'NtFavouritesModal',

    methods: {
      show() {
        this.$refs.modal.show()
      },
      async deleteFavourite(fileID) {
        await this.$api.DeleteFavourite(fileID)
          .then(response => {

            console.log('FAVOURITES DELETION SUCCESS:', response);
            // remove favourite from favourites.

            this.favourites = this.favourites.filter(function( obj ) {
                return obj.id != fileID;
            });

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
      async loadFavourites() {
        await this.$api.GetFavourites()
        .then(response => {
            console.log('FAVOURITES SUCCESS:', response);
            this.favourites = response.data;
          })
          .catch(e => {
            console.log('FAVOURITES ERROR', e.response);
          });
      },

      getIcon(icon) {
        // split into prefix and second name
        let src_icon = icon.split(" ")
        // it seems fontawesome is not happy with the fa-prefix
        src_icon[1] = src_icon[1].replace(/^fa-/gi, "");
        return src_icon
      },
    },
    data() {
      return {
        favourites: [],
      };
    },
    mounted() {
      // register the favourite popup
      EventBus.$on('favouriteModal', () => {
        this.show();
      });
    }
}
</script>

<style scoped>

.img-container-background {
  height: 150px;
  width: 100%;
  overflow: hidden;
  display:block;
  background: #191919;
  display: table;  
  position: relative;
  border-right: 1px solid rgba(0,0,0,0.5);
}

.img-container {  
  height: 150px;
  width: 100%;
  display: table-cell;  
  vertical-align: middle;
  text-align: center;
}

.img-container img {
  margin: auto;
  width: auto;
  height: auto;
  max-width: 100%;
  max-height: 100%;
}

.fav-options {
  display: none;
  position: absolute;
  top: 15%;
  right: 20px;
}

.delete-fav-btn, .copy-fav-btn, .open-fav-btn {
  background: transparent;
  border: none;
  transition: opacity 1s ease-in-out;
}

.delete-fav-btn:hover {
  background-color: #b50101;
}

.fav-card:hover .fav-options {
  display: block;
}

</style>
