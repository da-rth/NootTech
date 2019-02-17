<template>
  <div>
    <h1>wew you are signed in!</h1>
    <p style="color: white">
      Settings: {{ settings }}
      <br/>
      Files: {{ files }}
    </p>
    </div>
</template>

<script>
  export default {
    name: "AuthenticatedPane",
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
