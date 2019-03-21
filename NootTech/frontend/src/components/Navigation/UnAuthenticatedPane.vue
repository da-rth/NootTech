<template>
   <!--<nt-main-pane title="NootTech: More than meets the m-eye-nd" >-->
    <div class="container-fluid">
      <div class="row">
        <b-jumbotron header="Discover NootTech!"
          class="bg-dark welcome-pane"
          :container-fluid="true"
          :fluid="true"
          header-level=2
          lead="Uploading has never been easier">
          <b-carousel
            id="mainCarousel"
            style="text-shadow: 1px 1px 2px #333;"
            aria-controls="indicators"
            background="#ABABAB"
            :interval="5000"
            v-model="slide"
            :controls="true"
            @sliding-start="onSlideStart"
            @sliding-end="onSlideEnd"
          >
            <b-carousel-slide
              img-src="https://cdn.discordapp.com/attachments/543489677412401153/558303824096395264/unknown2.png"
            />
            <b-carousel-slide
              img-src="https://cdn.discordapp.com/attachments/543489677412401153/558304618237526027/unknown2.png"
            />
            <b-carousel-slide
              img-src="https://cdn.discordapp.com/attachments/543489677412401153/558305155569811458/unknown2.png"
            />
            <b-carousel-slide
              img-src="https://cdn.discordapp.com/attachments/543489677412401153/558306038449831942/unknown2.png"
            />
          </b-carousel>
          <br>
          <div class="row">
            <a href="https://discord.gg/xKquqD9"
              class="btn m-sm-auto m-md-auto m-lg-auto btn-lg">
                <font-awesome-icon :icon="['fab', 'discord']"/>
            </a>
            <a href="mailto:contact@noot.tech"
              class="btn m-sm-auto m-md-auto m-lg-auto btn-lg">
               <font-awesome-icon :icon="['fas', 'envelope']"/>
            </a>
            <a href="https://github.com/denBot/WAD2-Group-Project"
              class="btn m-sm-auto m-md-auto m-lg-auto btn-lg">
              <font-awesome-icon :icon="['fab', 'github']"/>
            </a>

          </div>
        </b-jumbotron>
      </div>
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
    background-color: #00000017 !important;
    border: 1px solid rgba(0,0,0,0.2);
    justify-content: center;
}

#mainCarousel {
  margin: 0 auto;
}
</style>
