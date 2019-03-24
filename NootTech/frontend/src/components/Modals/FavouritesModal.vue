<template>
    <b-modal
      id="favouritesModal"
      title="Favourited Files"
      header-bg-variant='dark'
      body-bg-variant='dark'
      footer-bg-variant='dark'
      @shown="loadFavourites"
      size="lg"
      :ok-only="true"
      ok-title="Close Favourites"
      scrollable
      centered
      >
      <h3 v-if="favourites.length == 0">You currently have no favourites.</h3>
      <b-card v-for="fav in favourites" :key="fav" no-body class="overflow-hidden fav-card">

        <a class="fav-href" :href="getShareLink(fav.username, fav.gen)">
        
        <b-row no-gutters>

          <b-col md="3">
            <div class="img-container-background">
              <div class="img-container">
                <img v-if="fav.thumbnail" :src="$backend_url+'/media/'+fav.thumbnail" class="img-responsive">
                <font-awesome-icon v-else :icon="getIcon(fav.icon)" style="font-size: 100px; padding: 10px;"/>
              </div>
            </div>
          </b-col>
          
          <b-col md="9">
            <b-card-body :title="fav.original">
              <b-card-text>
                Generated Filename: {{ fav.gen }}<br/>
                Uploaded by: {{ fav.username }}
              </b-card-text>
            </b-card-body>

          </b-col>
        </b-row>
        </a>

        <b-button title="Delete favourite" class="delete-fav-btn" v-on:click="deleteFavourite(fav.id)"><font-awesome-icon icon="trash-alt"/></b-button>

      </b-card>

    </b-modal>
</template>

<script>

export default {
    name: 'NtFavouritesModal',

    methods: {
      getShareLink (username, gen_id) {
        if (this.$subdomain_enabled) {
          return `${this.$site_url.replace("//","//"+username+".")}/${gen_id}`
        } else {
          return `${this.$site_url}/u/${username}/${gen_id}`
        }
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
              group: 'Global',
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
}
</script>

<style scoped>

.img-container-background {
  height: 130px;
  width: 100%;
  overflow: hidden;
  display:block;
  background: #191919;
  display: table;  
  position: relative;
  border-right: 1px solid rgba(0,0,0,0.5);
}

.img-container {  
  height: 130px;
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

.delete-fav-btn {
  background: transparent;
  border: none;
  transition: opacity 1s ease-in-out;
  display: none;
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 999;
}

.delete-fav-btn:hover {
  background-color: #b50101;
}

.fav-card:hover .delete-fav-btn {
  display: block;
}
.fav-card {
  background-color: #242424;
  margin: 5px;
}
.fav-href:hover {
  border: 2px solid #121212;
}

.fav-href:hover .delete-fav-btn {
  display: block;
}

.fav-href, .fav-href:visited, .fav-href:active {
  border: 2px solid transparent;
  color: transparent;
}
</style>
