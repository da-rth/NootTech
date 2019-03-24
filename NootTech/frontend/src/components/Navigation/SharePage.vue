<template>
  <div class="justify-content-center">
    
    <LoadingFiles v-if="isLoading == true" :multiple="false"/>

    <template v-else-if="this.file">

      <h2 class="file-header">{{ this.file.original_filename }}</h2>

      <VideoPlayer :file="file" v-if="file.file_video_info"/>
      <AudioPlayer :file="file" v-else-if="file.file_audio_info" class="AudioPlayerContainer"/>
      <ImagePreview :file="file" v-else-if="file.file_image_info"/>
      <TextPreview :file="file" v-else-if="file.file_text_info"/>

      <DownloadFile :file="file" />
      <br/><br/>
      <h4 class="file-header">File Information</h4>
      <FileInformation :file="file"/>
      <br/>
      <ReportFileModal :file="file"/>
      

      <div v-if="this.$store.state.user == null || this.$store.state.user.username != this.username" class="report-btn-container">
        <b-button class="report-btn" @click="onClick"><font-awesome-icon icon="flag"/>&nbsp; Report this file</b-button>
      </div>

      <br/><br/>
      <div v-if="this.$store.state.user != null">

        <b-button @click="toggleFavourite()" class="fav-btn">
          <template v-if="isFavourited">
            <font-awesome-icon icon="trash"/>&nbsp; Remove from Favourites
          </template>
          <template v-else>
            <font-awesome-icon icon="star"/>&nbsp; Add to Favourites
          </template>
        </b-button>

      </div>

      <br/><br/>
    </template>
    

    <div v-else class="private-container">
      <h1 class="private-msg">File is set to private or does not exist.</h1>
      <font-awesome-icon icon="sad-cry" class="big-sad" />
    </div>
  </div>
</template>

<script>
  import VideoPlayer from "../Utils/FilePreview/VideoPlayer";
  import AudioPlayer from "../Utils/FilePreview/AudioPlayer";
  import DownloadFile from "../Utils/FilePreview/DownloadFile";
  import ImagePreview from "../Utils/FilePreview/ImagePreview";
  import TextPreview from "../Utils/FilePreview/TextPreview";
  import FileInformation from "../Utils/FilePreview/FileInformation";
  import ReportFileModal from "../Modals/ReportFileModal";
  import LoadingFiles from '../FilePanel/LoadingFiles';

  import router from '../../router/index.js';

  export default {
    name: "ShareLinkPage",
    data () {
      return {
        file: '',
        colour: null,
        username: null,
        gen_name: null,
        isLoading: false,
        isFavourited: false
      }
    },
    components: {
      TextPreview,
      ImagePreview,
      DownloadFile,
      AudioPlayer,
      VideoPlayer,
      FileInformation,
      ReportFileModal,
      LoadingFiles
    },

    methods: {
      onClick () {
        this.$root.$emit('reportPopup', this.file);
      },
      
      getFavouriteElement() {
        let favourites = this.$root.favourite_files;
        for(var i = 0; i < favourites.length; i++) {
          if(favourites[i].gen == this.file.generated_filename)
            return favourites[i];
        }
        return null;
      },
      
      async toggleFavourite() {
       try {
         let favourite = this.getFavouriteElement();
         if(favourite != null) {
          await this.$api.DeleteFavourite(favourite.id);
         }
         else {
          await this.$api.AddFavourite(this.file.id);
         }
          await this.$api.GetFavourites()
          .then(response => {
            this.$root.favourite_files = response.data;
            this.isFavourited = this.checkFavourited();
          })
          .catch(e => {
            console.log(e.response.data);
            console.log('FAVOURITES ERROR...');
          });
        } catch(error) {
          console.log(error);
        }
      },

      checkFavourited() {
        let isPresent = false;
        for(var i = 0; i < this.$root.favourite_files.length; i++) {
            if (this.$root.favourite_files[i].gen ==  this.file.generated_filename) {
                isPresent = true;
                break;
            }
        }
        return isPresent;
      }
    },

    async beforeMount() {

        this.isLoading = true;
        this.isFavourited = this.checkFavourited();
        this.username = this.$route.params.username;
        this.gen_name = this.$route.params.gen_name;
        this.$root.sharelinkName = this.username;

        await this.$api.GetShareData(this.username, this.gen_name)
        .then(response => {
          this.file = response.data.file;
          this.$root.colour = response.data.colour;
          this.LoadingFiles = false;
        })
        .catch(e => {
          console.log(e.response.data);
          console.log('SHARELINK ERROR...');
          this.isLoading = false;
          router.push('/404');
        });


        await this.$api.GetFavourites()
        .then(response => {
          this.$root.favourite_files = response.data;
          this.isFavourited = this.checkFavourited();
        })
        .catch(e => {
          console.log(e.response.data);
          console.log('FAVOURITES ERROR...');
        });

        this.isLoading = false;
    },
    
    beforeDestroy() {
      this.$root.sharelinkName = null;
    },


  }
</script>

<style scoped>
* {
  font-family: 'Roboto', sans-serif;

}
  .file-header {
    text-align: center;
    margin: 20px;
    color: #fff;
    font-weight: 100;
  }

  .AudioPlayerContainer {
    margin: 0 100px;
  }
  .report-btn-container {
    padding: 40px;
    text-align: center;
  }

  .report-btn, .fav-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #202020;
    border: 1px solid #3d3d3d;
    margin: 0 auto;
    padding: 10px 30px;
  }

  .report-btn:hover {
    background-color: transparent;
    border-color: #FF0000;
    opacity: 0.9;
  }

  .private-container {
    padding: 50px;
    text-align: center;
  }

  .big-sad {
    margin: 20px;
    font-size: 150px;
  }
</style>
