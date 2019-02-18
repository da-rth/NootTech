<template>
  <div>
    <h1>wew you are signed in!</h1>
      Settings: {{ settings }}
      <br/>
      Files: {{files}}
      <br/>
      <nt-badge v-for="file in files" :key="file.id" :value="file"></nt-badge>
  </div>
</template>

<script>
  import NtBadge from '../Utils/Badge.vue'
  export default {
    name: "AuthenticatedPane",
    components: {NtBadge},
    data () {
      return {
        settings: null,
        files: null
      }
    },
    methods: {
      async getSettings() {
        this.settings = await this.$api.GetSettings();
        this.files = await this.$api.GetFiles();
      },
    },
    beforeMount () {
      this.getSettings()
      this.getFiles()
    },
  }
</script>

<style scoped>

</style>
