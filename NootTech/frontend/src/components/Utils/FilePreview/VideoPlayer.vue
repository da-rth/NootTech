<template>
  <div class="video-container">
  <video-player
    ref="videoPlayer"
    class="video-player-box vjs-big-play-centered NTVideoPlayer"
    :options="{ aspectRatio: '16:9', muted: false, language: 'en', playbackRates: [0.7, 1.0, 1.5, 2.0], sources: [{ src: video }], fluid: true }"
    :playsinline="true">
  </video-player>
    </div>
</template>

<script>
  // Similarly, you can also introduce the plugin resource pack you want to use within the component
  // import 'some-videojs-plugin'
  export default {
    props: ['file'],
    data() {
      return {
        video: this.file.file_content.startsWith('/') ? this.$backend_url+this.file.file_content : this.file.file_content
      }
    },
    computed: {
      player() {
        return this.$refs.videoPlayer.player
      }
    },
    methods: {
    }
  }
</script>

<style scoped>
  .video-container {
    background-color: #181818;
    border-top: 1px solid rgba(0,0,0,0.6);
    border-bottom: 1px solid rgba(0,0,0,0.6);
  }
.NTVideoPlayer {
  margin: 0 auto;
}
</style>
