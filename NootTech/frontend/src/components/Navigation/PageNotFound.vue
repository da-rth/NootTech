<template>
  <div class="ErrorPage" v-if="video">
    <div class="error-heading">Whoops, we couldn't find that page...</div>
    <div class="error-subheading">... so here's a random video!</div>
    <iframe class="custom-yt-player" v-bind:src="video.embed" frameborder="0" allow="autoplay; encrypted-media; loop;"></iframe>
    <div class="credits-container">Video: <a v-bind:href="video.url">{{ video.title }}</a> on YouTube.com</div>
  </div>
</template>

<script>
export default {
  name: 'PageNotFound',
  data () {
    return {
      video: null
    }
  },
  methods: {
    async getRandomVideo () {
      let videos = await this.$api.GetErrorVideos();
      this.video = videos[Math.floor(Math.random()*videos.length)];
      let tag = this.video.url.split('?v=')[1];
      this.video.embed = 'https://www.youtube.com/embed/'+tag+'?modestbranding=1&version=3&color=white&autoplay=1&loop=1&playlist='+tag+'&rel=0&showinfo=0&controls=0'
    },
  },
  beforeMount () {
    this.getRandomVideo()
  },
  mounted() {
    console.log('loaded page')
  }
}
</script>

<style scoped>
  .error-heading {
    text-align: center;
    font-size: 24px;
    color: #00cccc;
    margin-top: 30px;
  }
  .error-subheading {
    text-align: center;
    font-size: 14px;
    margin-bottom: 50px;
  }
  .custom-yt-player {
    margin: 0 auto;
    display: block;
  }
  @media (min-width: 0px) {
    .custom-yt-player {
      width: 100vw;
      height: 60vw;
    }
  }
  @media (min-width: 768px) {
    .custom-yt-player {
      width: 50vw;
      height: 30vw;
    }
  }
  .credits-container {
    padding-top: 50px;
    text-align: center;
    font-size: 13px;
    color: #787878;
  }
  .credits-container a {
    color: #00cccc;
  }
</style>
