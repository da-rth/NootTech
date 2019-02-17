<template>
  <nt-main-pane title="NootTech: More than meets the m-eye-nd" >
    <div v-if="$store.state.user.authenticated">
      <h1> You are logged in! Files will appear here</h1>
    </div>
    <div class="container-fluid" v-else>
      <div class="row">
        <b-jumbotron header="Discover NooTech!"
                class="bg-dark"
                lead="This is a simple hero unit">
          <b-carousel
            id="mainCarousel"
            style="text-shadow: 1px 1px 2px #333;"
            aria-controls="indicators"
            background="#ABABAB"
            :interval="3000"
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
  </nt-main-pane>
</template>

<script>
import NtMainPane from './Navigation/MainPane.vue';

export default {
    name: "Base",
    components: {NtMainPane},
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

</style>
