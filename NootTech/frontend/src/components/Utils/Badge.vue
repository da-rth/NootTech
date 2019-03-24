<template>

  <b-card
    overlay
    img-alg="Image"
    img-top
    tag="article"
    class="mb-2 hovereffect bg-dark"
    :border-variant="selected ? 'danger' : 'secondary'"
    v-bind:value="value"
    text-variant="dark"
    v-on:input="$emit('input', $event.target.value); "
    :img-src="value.file_thumbnail"
  >
    <font-awesome-icon 
     icon="play"
     v-if="value.file_thumbnail && value.file_mime_type.startsWith('video')" 
     class="large-fa-icon"
     />

    <font-awesome-icon 
     :icon="getIcon()" 
     v-else-if="value.file_thumbnail == null" 
     class="large-fa-icon"
    />
    
    <span class="gen-name" v-if="!value.file_thumbnail">{{ value.generated_filename }}</span>

    <div class="overlay" @click.stop="onClick">
      <h2 class="overlay-title">{{value.original_filename}}</h2>
      <div class="overlay-footer">
        <div class="icon">
          <font-awesome-icon :icon="getIcon()" v-if="value.file_thumbnail != null"/>
          <font-awesome-icon icon="file-archive" v-else/>
          <span style="padding-left: 2px">{{ value.file_size_str }}</span>
        </div>
        <div class="favoured" @click.stop="toggleFavourite()">
          <span v-if="is_favourite" class="favourite">⭐</span>
          <font-awesome-icon
            v-else
            :icon="getFavouriteIcon()"/>
        </div>

        <div class="views">
          <font-awesome-icon icon="eye"/>
          <span style="padding-left: 2px">{{getViews()}}</span>
        </div>
      </div>
    </div>
  </b-card>
</template>

<script>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
  import NtFilePopupModal from '../Modals/FilePopupModal'
  export default {
    name: "NtBadge",
    components: {FontAwesomeIcon, NtFilePopupModal},
    props: ['value', 'selected', 'selectionStatus'],
    data() {
      return {
        popup_id: 'popup-' + this.value.id,
        is_favourite: this.getFavouriteElement() != null
      }
    },
    methods: {
      getFavouriteElement() {
        let favourites = this.$root.favourite_files;
        for(var i = 0; i < favourites.length; i++) {
          if(favourites[i].gen == this.value.generated_filename)
            return favourites[i];
        }
        return null;
      },
      getIcon() {
        // split into prefix and second name
        let src_icon = this.value.icon.split(" ")
        // it seems fontawesome is not happy with the fa-prefix
        src_icon[1] = src_icon[1].replace(/^fa-/gi, "");
        return src_icon
      },
      getViews() {
        let views = this.value.views;
        if (views > 1e6)
          return (views / 1e6).toFixed(1) + "M";
        if(views > 1000)
          return (views / 1e3).toFixed(1) + "K";
        return views;
      },
      onClick() {
        if(this.selectionStatus) {
          this.selected ^= true;
          this.$root.toggleFile(this.value.id);
        }
        else
          this.$root.$emit('filePopupModal', this.value);
      },
      getFavouriteIcon() {
        return "star"
      },

      async toggleFavourite() {
       try {
         let favourite = this.getFavouriteElement();
         if(favourite != null) {
          await this.$api.DeleteFavourite(favourite.id);
         }
         else {
          await this.$api.AddFavourite(this.value.id);
         }
         this.is_favourite ^= true;
         this.$root.$emit('refreshFavourites');
        } catch(error) {
          this.$notify({
            title: "Whoops! Couldn't change your favourite settings!",
            text: "We are sending a team of specialised monkeys to fix this error!",
            position: "top right",
            type: "error"
          })
          console.log(error.response.data);
        }
      }
    }
  }
</script>

<style>

  .gen-name {
    opacity: 1;
    transition: opacity 0.5s;
    position: absolute;
    bottom: 10px;
    left: 0;
    right: 0;
  }
  .hovereffect:hover .gen-name {
    opacity: 0;
  }

  .hovereffect {
    background-size: cover;
    overflow: hidden;
    display: inline-block;
  }
  .hovereffect .overlay {
    width: 100%;
    height: 100%;
    position: absolute;
    overflow: hidden;
    display: inline-block;
    top: 0;
    left: 0;
    opacity: 0;
    background-color: rgba(0,0,0,0.3);
    -webkit-transition: all .4s ease-in-out;
    transition: all .4s ease-in-out;
  }
  .overlay-title {
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .overlay-footer {
    background: rbga(0, 0, 0, 0.6);
    color: lightgray;
    position: absolute;
    width: 100%;
    bottom: 0;
    padding: 0 0.5em 0.2em;
  }
  .icon {
    float: left;
  }
  .favoured {
    float: left;
    margin-left: 4px;
  }

  .favourite {
    color: yellow;
    font-family: Dejavu Sans;
  }
  .views {
    float:right;
  }
  .hovereffect:hover {
    cursor: pointer;
  }
  .hovereffect h2 {
    text-transform: uppercase;
    text-align: center;
    position: relative;
    font-size: 0.7em;
    color: lightgray;
    background:rgba(0,0,0,0.6);
    -webkit-transform:translatey(-100px);
    -ms-transform:translatey(-100px);
    transform:translatey(-100px);
    -webkit-transition:all .2s ease-in-out;
    transition:all .2s ease-in-out;
    padding:10px;
  }
  .hovereffect:hover img {
    -ms-transform:scale(1.2);
    -webkit-transform:scale(1.2);
    transform:scale(1.2);
  }
  .hovereffect:hover .overlay {
    opacity:1;
    filter: alpha(opacity=100)
  }
  .hovereffect:hover h2 {
    opacity: 1;
    filter: alpha(opacity=100);
    -ms-transform:translatey(0);
    -webkit-transform:translatey(0);
    transform: translatey(0);
  }
  .card-img-overlay {
    background-color: transparent;
    text-align: center;
  }

  .large-fa-icon {
    font-size: 400%;
    position: absolute;
    left: 50%;
    top: 50%;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
  }

  .badge-checkbox {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,.2);
  }

  .badge-checkbox .custom-control-label,
  .badge-checkbox .custom-control-label::before,
  .badge-checkbox .custom-control-label::after  {
    cursor: pointer;
    border-radius: 0px;
    width: 105% !important;
    height: auto !important;
    background: transparent !important;
    margin: -5px;
    position: absolute;
    left: 0;
    bottom: 0;
    top: 0;
  }
</style>
