<template>
   <!--<nt-main-pane title="NootTech: More than meets the m-eye-nd" >-->
    <div class="container-fluid">
      <div class="row">
        <b-jumbotron header="Discover NooTech!"
                class="bg-dark welcome-pane"
                lead="This is a simple hero unit">
          <b-carousel
            id="mainCarousel"
            style="text-shadow: 1px 1px 2px #333;"
            aria-controls="indicators"
            background="#ABABAB"
            :interval="5000"
            img-width="1024"
            img-height="480"
            v-model="slide"
            @sliding-start="onSlideStart"
            @sliding-end="onSlideEnd"
          >
            <b-carousel-slide
              text="Hi there, this is the first image"
              img-src="https://cdn.discordapp.com/attachments/543489677412401153/543489777220059136/1.jpg"
            />
            <b-carousel-slide
              text="Hi there, this is the second image"
              img-src="https://cdn.discordapp.com/attachments/543489677412401153/543489780923760644/2.jpg"
            />
            <b-carousel-slide
              text="Hi there, this is the third image"
              img-src="https://cdn.discordapp.com/attachments/543489677412401153/543489782706077696/99789.jpg"
            />
          </b-carousel>
          <br>
          <div class="row">
            <router-link
              to="/login"
              class="btn btn-primary m-sm-auto m-md-auto m-lg-auto">
                Get involved
            </router-link>
            <router-link
              to="/about"
              class="btn btn-primary m-sm-auto m-md-auto m-lg-auto">
                About us
            </router-link>
          </div>
        </b-jumbotron>
      </div>
    </div>
   <!--</nt-main-pane> -->
</template>

<script>
  export default {
    name: "AuthenticatedPane",
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
    }
  }
</script>

<style scoped>
  .welcome-pane {
    text-align: center;
    width: 90vw;
    background-color: #00000017 !important;
    border: 1px solid rgba(0,0,0,0.2);
    justify-content: center;
    margin: 40px auto;
}

#mainCarousel {
  width: 60vw;
  margin: 0 auto;
}
</style>
