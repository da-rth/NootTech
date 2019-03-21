<template>
   <!--<nt-main-pane title="NootTech: More than meets the m-eye-nd" >-->
    <div class="container-fluid">
      <div class="row">
        <b-jumbotron header="Welcome to NootTech!"
          class="welcome-pane"
          :container-fluid="true"
          :fluid="true"
          header-level=4
          >
          <br/>
          <h5>This is a place where anyone can store their files, both privately and publicly. Access and share your content easily from anywhere!</h5>
          <br/>
          <h5>Uploading has never been easier!</h5>
          <br/>
          <b-carousel
            id="mainCarousel"
            style="text-shadow: 1px 1px 2px #333;"
            class="homepage-carousel"
            aria-controls="indicators"
            background="#ABABAB"
            :interval="5000"
            v-model="slide"
            :controls="true"
            @sliding-start="onSlideStart"
            @sliding-end="onSlideEnd"
          >
            <b-carousel-slide :img-src="$backend_url+'/media/slider1.png'"/>
            <b-carousel-slide :img-src="$backend_url+'/media/slider2.png'"/>
            <b-carousel-slide :img-src="$backend_url+'/media/slider3.png'"/>
            <b-carousel-slide :img-src="$backend_url+'/media/slider4.png'"/>
          </b-carousel>
          <br><br>
          <h1>Have questions? Contact us!</h1>
          <br/>
          <div class="row">

            <a href="https://discord.gg/xKquqD9" class="large-icon">
                <font-awesome-icon :icon="['fab', 'discord']"/>
            </a>

            <a href="mailto:contact@noot.tech" class="large-icon">
               <font-awesome-icon :icon="['fas', 'envelope']"/>
            </a>

            <a href="https://github.com/denBot/WAD2-Group-Project" class="large-icon">
              <font-awesome-icon :icon="['fab', 'github']"/>
            </a>

          </div>
        </b-jumbotron>
      </div>
      <br/><br/>
    </div>
    
   <!--</nt-main-pane> -->
</template>

<script>
  export default {
    name: "UnAuthenticatedPane",
    data() {
      return {
        slide: 0,
        sliding: true
      }
    },
    // avoid looping
    methods: {
      onSlideStart(slide) { this.sliding = true},
      onSlideEnd(slide) { this.sliding = false}
    },
    async updated() {
      this.$root.colour = this.$root.default_colour;
      this.$root.sharelinkName = null;
    },
    async mounted() {
      this.$root.colour = this.$root.default_colour;
      this.$root.sharelinkName = null;
    }
  }
</script>

<style scoped>
  a {
    font-size: 3rem;
  }
  .welcome-pane {
    text-align: center;
    width: 90vw;
    background-color: #202020 !important;
    border: 1px solid rgba(0,0,0,0.2);
    margin: 30px;
    justify-content: center;
}

#mainCarousel {
  margin: 0 auto;
}
.large-icon {
  font-size: 100px;
  padding: 50px;
}

.large-icon svg {
  -webkit-transition: -webkit-transform .5s ease-in-out;
  -ms-transition: -ms-transform .5s ease-in-out;
  transition: transform .5s ease-in-out; 
}

.large-icon:hover svg {
  transform:rotate(360deg);
  -ms-transform:rotate(360deg);
  -webkit-transform:rotate(360deg);
  color: #fff;
}

.large-icon svg path {
  -webkit-transition: color .5s ease-in-out;
  -ms-transition: color .5s ease-in-out;
  transition: color .5s ease-in-out; 
}

.large-icon:hover svg path {
  color: white;
}

.homepage-carousel {
  width: 70%;
  max-width: 90%;
  border: 1px solid black;
}
</style>
